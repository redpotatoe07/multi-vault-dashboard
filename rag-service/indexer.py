"""
Indexer - Index entire vaults into ChromaDB with embeddings

This module handles:
- Batch indexing of all files in a vault
- Progress tracking
- Error handling
- Embedding generation via Ollama
- Efficient batch processing
"""

import ollama
from typing import List, Dict, Any, Optional, Callable
import logging
import json
import time
from pathlib import Path

from vector_store import VaultVectorStore
from metadata_extractor import MetadataExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VaultIndexer:
    """Index vault documents into ChromaDB with embeddings"""

    def __init__(
        self,
        vault_path: str,
        vault_name: str,
        vector_store: Optional[VaultVectorStore] = None,
        embedding_model: str = "nomic-embed-text",
        batch_size: int = 10
    ):
        """
        Initialize indexer for a specific vault

        Args:
            vault_path: Absolute path to vault directory
            vault_name: Name of the vault (used for collection name)
            vector_store: VaultVectorStore instance (creates new if None)
            embedding_model: Ollama model for embeddings (default: nomic-embed-text)
            batch_size: Number of documents to process in each batch
        """
        self.vault_path = Path(vault_path).resolve()
        self.vault_name = vault_name
        self.embedding_model = embedding_model
        self.batch_size = batch_size

        # Initialize components
        self.metadata_extractor = MetadataExtractor(str(self.vault_path))
        self.vector_store = vector_store or VaultVectorStore()

        logger.info(f"VaultIndexer initialized for '{vault_name}' at {vault_path}")

    def prepare_embedding_text(self, metadata: Dict[str, Any]) -> str:
        """
        Prepare text for embedding generation

        Combines key fields to create rich semantic representation

        Args:
            metadata: Metadata dictionary from MetadataExtractor

        Returns:
            Text string optimized for embedding
        """
        # Extract key information
        title = metadata['filename'].replace('.md', '')
        folder = metadata.get('folder', '')
        tags = ', '.join(metadata.get('all_tags', [])[:10])  # Limit to 10 tags
        content = metadata.get('content', '')[:1000]  # First 1000 chars

        # Get frontmatter fields that might be useful
        frontmatter = metadata.get('frontmatter', {})
        fm_type = frontmatter.get('type', '')
        fm_status = frontmatter.get('status', '')

        # Combine into embedding text
        embedding_text = f"""
Title: {title}
Folder: {folder}
Tags: {tags}
Type: {fm_type}
Status: {fm_status}
Content: {content}
        """.strip()

        return embedding_text

    def prepare_chroma_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare metadata for ChromaDB storage

        ChromaDB has limitations on metadata types, so we need to convert
        complex types to strings and ensure values are valid

        Args:
            metadata: Metadata dictionary from MetadataExtractor

        Returns:
            ChromaDB-compatible metadata dictionary
        """
        chroma_meta = {
            "file_path": metadata['file_path'],
            "filename": metadata['filename'],
            "folder": metadata['folder'],
            "folder_path": metadata.get('folder_path', ''),
            "word_count": metadata['word_count'],
            "created": metadata['created'],
            "modified": metadata['modified'],
            "wikilinks_count": metadata['wikilinks_count'],
            "heading_count": metadata['heading_count'],
        }

        # Add tags as JSON string
        if metadata.get('all_tags'):
            chroma_meta['tags'] = json.dumps(metadata['all_tags'])

        # Add select frontmatter fields
        frontmatter = metadata.get('frontmatter', {})
        if frontmatter.get('type'):
            chroma_meta['type'] = str(frontmatter['type'])
        if frontmatter.get('status'):
            chroma_meta['status'] = str(frontmatter['status'])

        return chroma_meta

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding using Ollama

        Args:
            text: Text to embed

        Returns:
            768-dimensional embedding vector
        """
        try:
            response = ollama.embeddings(
                model=self.embedding_model,
                prompt=text
            )
            return response['embedding']

        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise

    def index_document(self, metadata: Dict[str, Any]) -> bool:
        """
        Index a single document

        Args:
            metadata: Metadata dictionary from MetadataExtractor

        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare embedding text
            embedding_text = self.prepare_embedding_text(metadata)

            # Generate embedding
            embedding = self.generate_embedding(embedding_text)

            # Prepare ChromaDB metadata
            chroma_metadata = self.prepare_chroma_metadata(metadata)

            # Add to vector store
            self.vector_store.add_documents(
                collection_name=self.vault_name,
                documents=[metadata['content']],
                embeddings=[embedding],
                metadatas=[chroma_metadata],
                ids=[metadata['file_id']]
            )

            return True

        except Exception as e:
            logger.error(f"Failed to index {metadata.get('file_path', 'unknown')}: {e}")
            return False

    def index_batch(
        self,
        metadata_list: List[Dict[str, Any]],
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Dict[str, Any]:
        """
        Index a batch of documents

        Args:
            metadata_list: List of metadata dictionaries
            progress_callback: Optional callback function(current, total)

        Returns:
            Statistics about the indexing process
        """
        total = len(metadata_list)
        successful = 0
        failed = 0
        errors = []

        start_time = time.time()

        for i, metadata in enumerate(metadata_list, 1):
            try:
                success = self.index_document(metadata)
                if success:
                    successful += 1
                else:
                    failed += 1

            except Exception as e:
                failed += 1
                errors.append({
                    "file": metadata.get('file_path', 'unknown'),
                    "error": str(e)
                })
                logger.error(f"Error indexing document {i}/{total}: {e}")

            # Progress callback
            if progress_callback:
                progress_callback(i, total)

        elapsed_time = time.time() - start_time

        stats = {
            "total": total,
            "successful": successful,
            "failed": failed,
            "errors": errors,
            "elapsed_seconds": elapsed_time,
            "docs_per_second": successful / elapsed_time if elapsed_time > 0 else 0
        }

        return stats

    def index_vault(
        self,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        skip_existing: bool = True
    ) -> Dict[str, Any]:
        """
        Index all files in the vault

        Args:
            progress_callback: Optional callback function(current, total)
            skip_existing: Skip files already in the collection (default: True)

        Returns:
            Statistics about the indexing process
        """
        logger.info(f"Starting full vault indexing for '{self.vault_name}'...")

        # Get all vault files
        file_paths = self.metadata_extractor.get_vault_files()
        logger.info(f"Found {len(file_paths)} files to process")

        # Extract metadata for all files
        logger.info("Extracting metadata from all files...")
        all_metadata = self.metadata_extractor.extract_batch(file_paths)
        logger.info(f"Metadata extracted from {len(all_metadata)} files")

        # Skip existing files if requested
        if skip_existing:
            collection = self.vector_store.get_or_create_collection(self.vault_name)
            existing_count = collection.count()

            if existing_count > 0:
                logger.info(f"Collection already contains {existing_count} documents")
                # For now, we'll re-index all. In production, we'd check IDs
                # and only index new/modified files

        # Index in batches
        total_stats = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "errors": [],
            "elapsed_seconds": 0
        }

        # Process in batches to show progress
        for i in range(0, len(all_metadata), self.batch_size):
            batch = all_metadata[i:i + self.batch_size]
            batch_num = (i // self.batch_size) + 1
            total_batches = (len(all_metadata) + self.batch_size - 1) // self.batch_size

            logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} files)...")

            batch_stats = self.index_batch(batch, progress_callback)

            # Aggregate stats
            total_stats["total"] += batch_stats["total"]
            total_stats["successful"] += batch_stats["successful"]
            total_stats["failed"] += batch_stats["failed"]
            total_stats["errors"].extend(batch_stats["errors"])
            total_stats["elapsed_seconds"] += batch_stats["elapsed_seconds"]

        # Calculate final stats
        total_stats["docs_per_second"] = (
            total_stats["successful"] / total_stats["elapsed_seconds"]
            if total_stats["elapsed_seconds"] > 0 else 0
        )

        logger.info(f"Indexing complete! {total_stats['successful']}/{total_stats['total']} documents indexed")

        return total_stats

    def reindex_document(self, file_path: str) -> bool:
        """
        Re-index a single document (update if exists, add if new)

        Args:
            file_path: Absolute path to the file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Extract metadata
            metadata = self.metadata_extractor.extract(file_path)

            # Prepare data
            embedding_text = self.prepare_embedding_text(metadata)
            embedding = self.generate_embedding(embedding_text)
            chroma_metadata = self.prepare_chroma_metadata(metadata)

            # Try to update first (if exists), otherwise add
            try:
                self.vector_store.update_document(
                    collection_name=self.vault_name,
                    document_id=metadata['file_id'],
                    document=metadata['content'],
                    embedding=embedding,
                    metadata=chroma_metadata
                )
                logger.info(f"Updated: {metadata['file_path']}")

            except Exception:
                # Document doesn't exist, add it
                self.vector_store.add_documents(
                    collection_name=self.vault_name,
                    documents=[metadata['content']],
                    embeddings=[embedding],
                    metadatas=[chroma_metadata],
                    ids=[metadata['file_id']]
                )
                logger.info(f"Added: {metadata['file_path']}")

            return True

        except Exception as e:
            logger.error(f"Failed to reindex {file_path}: {e}")
            return False

    def delete_document(self, file_path: str) -> bool:
        """
        Delete a document from the index

        Args:
            file_path: Relative path from vault root

        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert file path to document ID
            file_id = file_path.replace('/', '_').replace('\\', '_').replace('.md', '')

            self.vector_store.delete_document(
                collection_name=self.vault_name,
                document_id=file_id
            )

            logger.info(f"Deleted: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete {file_path}: {e}")
            return False
