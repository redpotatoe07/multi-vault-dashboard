"""
RAG Service API - Flask REST API for Multi-Vault RAG System

This provides HTTP endpoints for:
- Hybrid search across vaults
- Indexing management
- File watcher control
- Collection status
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from pathlib import Path

from vector_store import VaultVectorStore
from indexer import VaultIndexer
from hybrid_search import HybridSearch
from file_watcher import VaultWatcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for dashboard

# Global instances
vector_store = None
hybrid_search = None
active_watchers = {}  # {vault_name: watcher_instance}
active_indexers = {}  # {vault_name: indexer_instance}

# Configuration
VAULT_ROOT = r"C:\Users\redpo\repos\Obsidian\Multi-Vault"
CHROMA_DB_PATH = "./chroma_db"


def initialize():
    """Initialize global instances"""
    global vector_store, hybrid_search

    logger.info("Initializing RAG Service...")

    # Initialize vector store
    vector_store = VaultVectorStore(persist_directory=CHROMA_DB_PATH)
    logger.info(f"Vector store initialized at: {CHROMA_DB_PATH}")

    # Initialize hybrid search
    hybrid_search = HybridSearch(vector_store)
    logger.info("Hybrid search initialized")


def get_vault_path(vault_name: str) -> str:
    """Get absolute path to vault"""
    # Try with .vault extension first
    vault_path = Path(VAULT_ROOT) / f"{vault_name}.vault"
    if vault_path.exists():
        return str(vault_path)

    # Try without extension
    vault_path = Path(VAULT_ROOT) / vault_name
    if vault_path.exists():
        return str(vault_path)

    raise ValueError(f"Vault not found: {vault_name}")


def get_indexer(vault_name: str) -> VaultIndexer:
    """Get or create indexer for a vault"""
    if vault_name not in active_indexers:
        vault_path = get_vault_path(vault_name)
        indexer = VaultIndexer(
            vault_path=vault_path,
            vault_name=vault_name,
            vector_store=vector_store
        )
        active_indexers[vault_name] = indexer

    return active_indexers[vault_name]


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "rag-service",
        "version": "0.3.0"
    })


@app.route('/search', methods=['POST'])
def search():
    """
    Search a vault using hybrid search

    Request body:
    {
        "vault_name": "ThistleRidgeHall",
        "query": "what are all the artworks?",
        "explain": false
    }

    Response:
    {
        "query": "what are all the artworks?",
        "query_type": "list_all",
        "search_strategy": "metadata_only",
        "results": [...],
        "result_count": 47
    }
    """
    try:
        data = request.json
        vault_name = data.get('vault_name')
        query = data.get('query')
        explain = data.get('explain', False)

        if not vault_name or not query:
            return jsonify({"error": "vault_name and query are required"}), 400

        # Perform search
        results = hybrid_search.search(
            vault_name=vault_name,
            query=query,
            explain=explain
        )

        return jsonify(results)

    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/index', methods=['POST'])
def index_vault():
    """
    Index a vault

    Request body:
    {
        "vault_name": "ThistleRidgeHall",
        "batch_size": 10,
        "skip_existing": true
    }

    Response:
    {
        "status": "success",
        "stats": {
            "total": 277,
            "successful": 277,
            "failed": 0,
            "elapsed_seconds": 26.9
        }
    }
    """
    try:
        data = request.json
        vault_name = data.get('vault_name')
        batch_size = data.get('batch_size', 10)
        skip_existing = data.get('skip_existing', True)

        if not vault_name:
            return jsonify({"error": "vault_name is required"}), 400

        # Get indexer
        indexer = get_indexer(vault_name)

        # Index vault
        logger.info(f"Starting indexing for vault: {vault_name}")
        stats = indexer.index_vault(skip_existing=skip_existing)

        return jsonify({
            "status": "success",
            "vault_name": vault_name,
            "stats": stats
        })

    except Exception as e:
        logger.error(f"Indexing error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/status', methods=['GET'])
def get_status():
    """
    Get collection status

    Query params:
    - vault_name: Name of the vault

    Response:
    {
        "vault_name": "ThistleRidgeHall",
        "status": "indexed",
        "document_count": 277,
        "watcher_active": false
    }
    """
    try:
        vault_name = request.args.get('vault_name')

        if not vault_name:
            return jsonify({"error": "vault_name parameter is required"}), 400

        # Get collection stats
        stats = vector_store.get_collection_stats(vault_name)

        # Check if watcher is active
        watcher_active = vault_name in active_watchers and active_watchers[vault_name].is_running

        return jsonify({
            "vault_name": vault_name,
            "status": "indexed" if stats['count'] > 0 else "not_indexed",
            "document_count": stats['count'],
            "watcher_active": watcher_active,
            "collection_metadata": stats['metadata']
        })

    except Exception as e:
        logger.error(f"Status error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/collections', methods=['GET'])
def list_collections():
    """
    List all collections

    Response:
    {
        "collections": [
            {
                "name": "ThistleRidgeHall",
                "document_count": 277
            }
        ]
    }
    """
    try:
        collection_names = vector_store.list_collections()

        collections = []
        for name in collection_names:
            stats = vector_store.get_collection_stats(name)
            collections.append({
                "name": name,
                "document_count": stats['count']
            })

        return jsonify({"collections": collections})

    except Exception as e:
        logger.error(f"List collections error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/watcher/start', methods=['POST'])
def start_watcher():
    """
    Start file watcher for a vault

    Request body:
    {
        "vault_name": "ThistleRidgeHall"
    }

    Response:
    {
        "status": "started",
        "vault_name": "ThistleRidgeHall"
    }
    """
    try:
        data = request.json
        vault_name = data.get('vault_name')

        if not vault_name:
            return jsonify({"error": "vault_name is required"}), 400

        # Check if watcher already running
        if vault_name in active_watchers and active_watchers[vault_name].is_running:
            return jsonify({
                "status": "already_running",
                "vault_name": vault_name
            })

        # Get indexer
        indexer = get_indexer(vault_name)

        # Create and start watcher
        watcher = VaultWatcher(indexer=indexer)
        watcher.start()

        active_watchers[vault_name] = watcher

        logger.info(f"Started watcher for vault: {vault_name}")

        return jsonify({
            "status": "started",
            "vault_name": vault_name
        })

    except Exception as e:
        logger.error(f"Start watcher error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/watcher/stop', methods=['POST'])
def stop_watcher():
    """
    Stop file watcher for a vault

    Request body:
    {
        "vault_name": "ThistleRidgeHall"
    }

    Response:
    {
        "status": "stopped",
        "vault_name": "ThistleRidgeHall"
    }
    """
    try:
        data = request.json
        vault_name = data.get('vault_name')

        if not vault_name:
            return jsonify({"error": "vault_name is required"}), 400

        # Check if watcher exists
        if vault_name not in active_watchers:
            return jsonify({
                "status": "not_running",
                "vault_name": vault_name
            })

        # Stop watcher
        watcher = active_watchers[vault_name]
        watcher.stop()

        del active_watchers[vault_name]

        logger.info(f"Stopped watcher for vault: {vault_name}")

        return jsonify({
            "status": "stopped",
            "vault_name": vault_name
        })

    except Exception as e:
        logger.error(f"Stop watcher error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/reindex', methods=['POST'])
def reindex_document():
    """
    Re-index a single document

    Request body:
    {
        "vault_name": "ThistleRidgeHall",
        "file_path": "Artworks/And What of the Apple Trees.md"
    }

    Response:
    {
        "status": "success",
        "file_path": "Artworks/And What of the Apple Trees.md"
    }
    """
    try:
        data = request.json
        vault_name = data.get('vault_name')
        file_path = data.get('file_path')

        if not vault_name or not file_path:
            return jsonify({"error": "vault_name and file_path are required"}), 400

        # Get indexer
        indexer = get_indexer(vault_name)

        # Get absolute file path
        vault_path = get_vault_path(vault_name)
        absolute_path = Path(vault_path) / file_path

        if not absolute_path.exists():
            return jsonify({"error": f"File not found: {file_path}"}), 404

        # Re-index
        success = indexer.reindex_document(str(absolute_path))

        if success:
            return jsonify({
                "status": "success",
                "file_path": file_path
            })
        else:
            return jsonify({
                "status": "failed",
                "file_path": file_path
            }), 500

    except Exception as e:
        logger.error(f"Reindex error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Initialize on startup
    initialize()

    # Run Flask app
    logger.info("Starting RAG Service on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=False)
