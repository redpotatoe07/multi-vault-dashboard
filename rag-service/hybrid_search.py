"""
HybridSearch - Combine semantic, keyword, and metadata search

This module implements intelligent hybrid search that adapts based on query type:
- LIST_ALL queries: Use metadata filtering only
- FILTER queries: Metadata-based filtering
- SEARCH queries: Combine semantic + keyword + metadata
- SPECIFIC queries: Focused semantic + keyword search
"""

import ollama
from typing import List, Dict, Any, Optional
import logging
import json
import re

from vector_store import VaultVectorStore
from query_router import QueryRouter, QueryType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HybridSearch:
    """Intelligent hybrid search combining multiple strategies"""

    def __init__(
        self,
        vector_store: VaultVectorStore,
        embedding_model: str = "nomic-embed-text"
    ):
        """
        Initialize hybrid search

        Args:
            vector_store: VaultVectorStore instance
            embedding_model: Ollama model for embeddings
        """
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.query_router = QueryRouter()

        logger.info("HybridSearch initialized")

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for search query

        Args:
            query: Search query string

        Returns:
            768-dimensional embedding vector
        """
        try:
            response = ollama.embeddings(
                model=self.embedding_model,
                prompt=query
            )
            return response['embedding']

        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            raise

    def metadata_filter_search(
        self,
        vault_name: str,
        folder: Optional[str] = None,
        tags: Optional[List[str]] = None,
        entity: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search using metadata filters only (for LIST_ALL queries)

        Args:
            vault_name: Name of the vault collection
            folder: Folder to filter by
            tags: Tags to filter by
            entity: Entity/type to filter by (e.g., "artworks", "characters")
            limit: Maximum results

        Returns:
            List of matching documents with metadata
        """
        logger.info(f"Metadata filter search: folder={folder}, tags={tags}, entity={entity}")

        # Build metadata filter
        where_filter = {}

        if folder:
            where_filter["folder"] = folder

        # For LIST_ALL queries, we use folder as the primary filter
        # Entity like "artworks" typically corresponds to "Artworks" folder
        if entity and not folder:
            # Try to map entity to folder name
            entity_folder_map = {
                "artwork": "Artworks",
                "artworks": "Artworks",
                "character": "Characters",
                "characters": "Characters",
                "location": "Locations",
                "locations": "Locations",
                "plot": "Plot",
                "plots": "Plot",
                "event": "Events",
                "events": "Events",
            }

            entity_lower = entity.lower()
            if entity_lower in entity_folder_map:
                where_filter["folder"] = entity_folder_map[entity_lower]

        # Get collection
        collection = self.vector_store.get_or_create_collection(vault_name)

        # If we have filters, use them
        if where_filter:
            try:
                results = collection.get(
                    where=where_filter,
                    limit=limit
                )

                # Convert to standard format
                formatted_results = []
                for i in range(len(results['ids'])):
                    formatted_results.append({
                        "id": results['ids'][i],
                        "metadata": results['metadatas'][i],
                        "document": results['documents'][i] if 'documents' in results else "",
                        "score": 1.0,  # Perfect match for metadata filter
                        "search_type": "metadata_filter"
                    })

                logger.info(f"Metadata filter found {len(formatted_results)} results")
                return formatted_results

            except Exception as e:
                logger.error(f"Metadata filter search failed: {e}")
                # Fall back to getting all and filtering manually
                return self._fallback_metadata_search(collection, where_filter, limit)

        else:
            # No filters - return all documents
            logger.warning("No metadata filters provided, returning all documents")
            all_results = collection.get(limit=limit)

            formatted_results = []
            for i in range(len(all_results['ids'])):
                formatted_results.append({
                    "id": all_results['ids'][i],
                    "metadata": all_results['metadatas'][i],
                    "document": all_results['documents'][i] if 'documents' in all_results else "",
                    "score": 1.0,
                    "search_type": "metadata_all"
                })

            return formatted_results

    def _fallback_metadata_search(
        self,
        collection,
        where_filter: Dict,
        limit: int
    ) -> List[Dict[str, Any]]:
        """Fallback method for metadata filtering"""
        try:
            # Get all documents
            all_results = collection.get(limit=limit * 2)

            # Filter manually
            filtered = []
            for i in range(len(all_results['ids'])):
                metadata = all_results['metadatas'][i]
                matches = True

                for key, value in where_filter.items():
                    if metadata.get(key) != value:
                        matches = False
                        break

                if matches:
                    filtered.append({
                        "id": all_results['ids'][i],
                        "metadata": metadata,
                        "document": all_results['documents'][i] if 'documents' in all_results else "",
                        "score": 1.0,
                        "search_type": "metadata_filter_fallback"
                    })

                    if len(filtered) >= limit:
                        break

            return filtered

        except Exception as e:
            logger.error(f"Fallback metadata search failed: {e}")
            return []

    def semantic_search(
        self,
        vault_name: str,
        query: str,
        limit: int = 20,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic similarity search

        Args:
            vault_name: Name of the vault collection
            query: Search query
            limit: Maximum results
            where: Optional metadata filter

        Returns:
            List of similar documents with scores
        """
        logger.info(f"Semantic search: query='{query}', limit={limit}")

        # Generate query embedding
        query_embedding = self.generate_query_embedding(query)

        # Search ChromaDB
        results = self.vector_store.query(
            collection_name=vault_name,
            query_embeddings=[query_embedding],
            n_results=limit,
            where=where
        )

        # Format results
        formatted_results = []
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                # Convert distance to similarity score (inverse)
                distance = results['distances'][0][i]
                similarity = 1 / (1 + distance)  # Normalize to 0-1

                formatted_results.append({
                    "id": results['ids'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "document": results['documents'][0][i],
                    "score": similarity,
                    "distance": distance,
                    "search_type": "semantic"
                })

        logger.info(f"Semantic search found {len(formatted_results)} results")
        return formatted_results

    def hybrid_search(
        self,
        vault_name: str,
        query: str,
        routing: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search based on query routing

        Args:
            vault_name: Name of the vault collection
            query: Search query
            routing: Routing information from QueryRouter

        Returns:
            Ranked list of results
        """
        query_type = routing['query_type']
        params = routing['parameters']
        strategy = routing['search_strategy']

        logger.info(f"Hybrid search: type={query_type.value}, strategy={strategy}")

        # Route to appropriate search strategy
        if strategy == "metadata_only" or strategy == "metadata_filter":
            # LIST_ALL or FILTER queries - use metadata only
            return self.metadata_filter_search(
                vault_name=vault_name,
                folder=routing.get('folder'),
                tags=routing.get('tags'),
                entity=routing.get('entity'),
                limit=params.get('limit', 100)
            )

        elif strategy == "semantic_only":
            # FIND_SIMILAR queries - pure semantic search
            return self.semantic_search(
                vault_name=vault_name,
                query=query,
                limit=params.get('limit', 15)
            )

        elif strategy == "semantic_keyword":
            # SPECIFIC queries - semantic with optional metadata filter
            where_filter = None
            if routing.get('folder'):
                where_filter = {"folder": routing['folder']}

            return self.semantic_search(
                vault_name=vault_name,
                query=query,
                limit=params.get('limit', 10),
                where=where_filter
            )

        else:  # hybrid
            # SEARCH queries - combine semantic and metadata
            where_filter = {}
            if routing.get('folder'):
                where_filter["folder"] = routing['folder']

            results = self.semantic_search(
                vault_name=vault_name,
                query=query,
                limit=params.get('limit', 20),
                where=where_filter if where_filter else None
            )

            return results

    def search(
        self,
        vault_name: str,
        query: str,
        explain: bool = False
    ) -> Dict[str, Any]:
        """
        Main search entry point

        Args:
            vault_name: Name of the vault collection
            query: Search query
            explain: Include routing explanation in results

        Returns:
            Dictionary with results and metadata
        """
        # Route the query
        routing = self.query_router.route_query(query)

        # Perform search
        results = self.hybrid_search(vault_name, query, routing)

        # Build response
        response = {
            "query": query,
            "query_type": routing['query_type'].value,
            "search_strategy": routing['search_strategy'],
            "results": results,
            "result_count": len(results)
        }

        if explain:
            response["routing_explanation"] = self.query_router.explain_routing(routing)
            # Convert routing dict to JSON-serializable format
            serializable_routing = dict(routing)
            serializable_routing['query_type'] = routing['query_type'].value
            response["routing"] = serializable_routing

        return response
