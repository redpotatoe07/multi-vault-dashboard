"""
MetadataExtractor - Extract metadata from Obsidian markdown files

This module parses markdown files and extracts:
- YAML frontmatter (tags, custom fields)
- File statistics (size, dates, word count)
- Folder structure
- Content (for embedding generation)
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import frontmatter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetadataExtractor:
    """Extract rich metadata from Obsidian markdown files"""

    def __init__(self, vault_root: str):
        """
        Initialize extractor for a specific vault

        Args:
            vault_root: Absolute path to vault root directory
        """
        self.vault_root = Path(vault_root).resolve()

        if not self.vault_root.exists():
            raise ValueError(f"Vault root does not exist: {vault_root}")

        logger.info(f"MetadataExtractor initialized for: {self.vault_root}")

    def extract(self, file_path: str) -> Dict[str, Any]:
        """
        Extract all metadata from a markdown file

        Args:
            file_path: Absolute path to the markdown file

        Returns:
            Dictionary containing all extracted metadata
        """
        file_path_obj = Path(file_path).resolve()

        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read file with frontmatter parsing
        with open(file_path_obj, 'r', encoding='utf-8', errors='ignore') as f:
            post = frontmatter.load(f)

        # Get file statistics
        stat = os.stat(file_path_obj)

        # Calculate relative path from vault root
        try:
            relative_path = file_path_obj.relative_to(self.vault_root)
        except ValueError:
            # File is outside vault root
            relative_path = file_path_obj

        # Extract folder hierarchy
        folder_parts = list(relative_path.parent.parts) if relative_path.parent != Path('.') else []
        folder = folder_parts[-1] if folder_parts else "root"

        # Extract content metadata
        content = post.content
        word_count = len(content.split())
        char_count = len(content)

        # Extract links (wikilinks and markdown links)
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)

        # Extract tags from content (Obsidian style #tags)
        content_tags = re.findall(r'#(\w+)', content)

        # Extract headings
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)

        # Build metadata dictionary
        metadata = {
            # File identification
            "file_path": str(relative_path).replace('\\', '/'),
            "filename": file_path_obj.name,
            "file_id": str(relative_path).replace('\\', '/').replace('/', '_').replace('.md', ''),

            # Folder structure
            "folder": folder,
            "folder_path": str(relative_path.parent).replace('\\', '/') if relative_path.parent != Path('.') else "",
            "folder_hierarchy": folder_parts,

            # File statistics
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "size_bytes": stat.st_size,

            # Content metadata
            "content": content,
            "word_count": word_count,
            "char_count": char_count,
            "line_count": content.count('\n') + 1,

            # Frontmatter
            "frontmatter": dict(post.metadata),
            "tags": post.metadata.get('tags', []) if isinstance(post.metadata.get('tags'), list) else [],

            # Content analysis
            "content_tags": list(set(content_tags)),  # Unique tags from content
            "wikilinks": wikilinks,
            "wikilinks_count": len(wikilinks),
            "markdown_links": [{"text": link[0], "url": link[1]} for link in markdown_links],
            "headings": headings,
            "heading_count": len(headings),

            # Combined tags (from frontmatter and content)
            "all_tags": list(set(post.metadata.get('tags', []) if isinstance(post.metadata.get('tags'), list) else []) | set(content_tags))
        }

        return metadata

    def extract_batch(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Extract metadata from multiple files

        Args:
            file_paths: List of absolute paths to markdown files

        Returns:
            List of metadata dictionaries
        """
        results = []
        errors = []

        for file_path in file_paths:
            try:
                metadata = self.extract(file_path)
                results.append(metadata)
            except Exception as e:
                logger.error(f"Failed to extract metadata from {file_path}: {e}")
                errors.append({"file": file_path, "error": str(e)})

        if errors:
            logger.warning(f"Encountered {len(errors)} errors during batch extraction")

        return results

    def get_vault_files(self, extensions: Optional[List[str]] = None) -> List[str]:
        """
        Get all markdown files in the vault

        Args:
            extensions: List of file extensions to include (default: ['.md'])

        Returns:
            List of absolute file paths
        """
        if extensions is None:
            extensions = ['.md']

        files = []
        for ext in extensions:
            files.extend(self.vault_root.rglob(f'*{ext}'))

        # Filter out files in .obsidian and other hidden directories
        files = [
            str(f) for f in files
            if not any(part.startswith('.') for part in f.parts)
        ]

        logger.info(f"Found {len(files)} files in vault")
        return files

    def extract_vault(self) -> List[Dict[str, Any]]:
        """
        Extract metadata from all markdown files in the vault

        Returns:
            List of metadata dictionaries for all vault files
        """
        file_paths = self.get_vault_files()
        logger.info(f"Extracting metadata from {len(file_paths)} files...")

        metadata_list = self.extract_batch(file_paths)

        logger.info(f"Successfully extracted metadata from {len(metadata_list)} files")
        return metadata_list
