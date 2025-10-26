"""
FileWatcher - Monitor vault for file changes and auto-index

This module uses watchdog to monitor the vault directory and automatically:
- Index new files when created
- Re-index files when modified
- Remove files from index when deleted
"""

import time
import threading
from pathlib import Path
from typing import Optional, Callable
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent

from indexer import VaultIndexer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VaultFileHandler(FileSystemEventHandler):
    """Handle file system events for vault files"""

    def __init__(
        self,
        indexer: VaultIndexer,
        debounce_seconds: float = 2.0,
        on_change_callback: Optional[Callable] = None
    ):
        """
        Initialize file handler

        Args:
            indexer: VaultIndexer instance
            debounce_seconds: Wait time before processing changes (default: 2s)
            on_change_callback: Optional callback function(event_type, file_path)
        """
        super().__init__()
        self.indexer = indexer
        self.debounce_seconds = debounce_seconds
        self.on_change_callback = on_change_callback

        # Track pending changes (debouncing)
        self.pending_changes = {}  # {file_path: (event_type, timestamp)}

        logger.info(f"VaultFileHandler initialized (debounce: {debounce_seconds}s)")

    def _should_process_file(self, file_path: str) -> bool:
        """
        Check if file should be processed

        Args:
            file_path: Path to the file

        Returns:
            True if file should be indexed
        """
        path = Path(file_path)

        # Only process markdown files
        if path.suffix.lower() != '.md':
            return False

        # Ignore hidden files and directories
        if any(part.startswith('.') for part in path.parts):
            return False

        # Ignore temp files
        if path.name.startswith('~') or path.name.endswith('~'):
            return False

        return True

    def _add_pending_change(self, event_type: str, file_path: str):
        """
        Add a pending change (for debouncing)

        Args:
            event_type: Type of event (created, modified, deleted)
            file_path: Path to the file
        """
        self.pending_changes[file_path] = (event_type, time.time())
        logger.debug(f"Pending change: {event_type} - {file_path}")

    def process_pending_changes(self):
        """
        Process all pending changes that have passed the debounce period
        """
        current_time = time.time()
        processed = []

        for file_path, (event_type, timestamp) in list(self.pending_changes.items()):
            # Check if debounce period has passed
            if current_time - timestamp >= self.debounce_seconds:
                self._process_change(event_type, file_path)
                processed.append(file_path)

        # Remove processed changes
        for file_path in processed:
            del self.pending_changes[file_path]

    def _process_change(self, event_type: str, file_path: str):
        """
        Process a file change

        Args:
            event_type: Type of event (created, modified, deleted)
            file_path: Path to the file
        """
        try:
            if event_type == 'deleted':
                # Remove from index
                # Convert absolute path to relative path
                path = Path(file_path)
                vault_root = Path(self.indexer.vault_path)

                try:
                    relative_path = path.relative_to(vault_root)
                    self.indexer.delete_document(str(relative_path).replace('\\', '/'))
                    logger.info(f"Removed from index: {relative_path}")
                except ValueError:
                    logger.warning(f"File outside vault root: {file_path}")

            elif event_type in ['created', 'modified']:
                # Re-index the file
                success = self.indexer.reindex_document(file_path)
                if success:
                    logger.info(f"{'Indexed' if event_type == 'created' else 'Re-indexed'}: {Path(file_path).name}")
                else:
                    logger.error(f"Failed to index: {file_path}")

            # Call callback if provided
            if self.on_change_callback:
                self.on_change_callback(event_type, file_path)

        except Exception as e:
            logger.error(f"Error processing {event_type} for {file_path}: {e}")

    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return

        if self._should_process_file(event.src_path):
            self._add_pending_change('created', event.src_path)

    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return

        if self._should_process_file(event.src_path):
            self._add_pending_change('modified', event.src_path)

    def on_deleted(self, event):
        """Handle file deletion events"""
        if event.is_directory:
            return

        if self._should_process_file(event.src_path):
            self._add_pending_change('deleted', event.src_path)


class VaultWatcher:
    """Watch a vault directory for changes and auto-index"""

    def __init__(
        self,
        indexer: VaultIndexer,
        debounce_seconds: float = 2.0,
        on_change_callback: Optional[Callable] = None
    ):
        """
        Initialize vault watcher

        Args:
            indexer: VaultIndexer instance
            debounce_seconds: Wait time before processing changes
            on_change_callback: Optional callback function(event_type, file_path)
        """
        self.indexer = indexer
        self.vault_path = str(indexer.vault_path)
        self.debounce_seconds = debounce_seconds

        # Create event handler and observer
        self.event_handler = VaultFileHandler(
            indexer=indexer,
            debounce_seconds=debounce_seconds,
            on_change_callback=on_change_callback
        )
        self.observer = Observer()
        self._processing_thread = None

        self.is_running = False

        logger.info(f"VaultWatcher initialized for: {self.vault_path}")

    def _processing_loop(self, process_interval: float = 1.0):
        """
        Background thread that processes pending changes

        Args:
            process_interval: How often to check for pending changes (seconds)
        """
        logger.info("Processing thread started")
        while self.is_running:
            try:
                self.event_handler.process_pending_changes()
                time.sleep(process_interval)
            except Exception as e:
                logger.error(f"Error in processing loop: {e}")
                time.sleep(process_interval)
        logger.info("Processing thread stopped")

    def start(self):
        """Start watching the vault directory"""
        if self.is_running:
            logger.warning("Watcher already running")
            return

        # Schedule observer
        self.observer.schedule(
            self.event_handler,
            self.vault_path,
            recursive=True
        )

        # Start observer
        self.observer.start()
        self.is_running = True

        # Start background processing thread
        self._processing_thread = threading.Thread(
            target=self._processing_loop,
            daemon=True,
            name=f"WatcherProcessor-{Path(self.vault_path).name}"
        )
        self._processing_thread.start()

        logger.info(f"Started watching: {self.vault_path}")

    def stop(self):
        """Stop watching the vault directory"""
        if not self.is_running:
            return

        # Signal threads to stop
        self.is_running = False

        # Stop observer
        self.observer.stop()
        self.observer.join()

        # Wait for processing thread to finish
        if self._processing_thread and self._processing_thread.is_alive():
            self._processing_thread.join(timeout=5.0)

        logger.info("Stopped watching vault")

    def process_pending(self):
        """Manually process pending changes (useful for testing)"""
        self.event_handler.process_pending_changes()

    def run(self, process_interval: float = 1.0):
        """
        Run the watcher in a loop (blocking)

        Args:
            process_interval: How often to check for pending changes (seconds)
        """
        self.start()

        try:
            while True:
                time.sleep(process_interval)
                self.event_handler.process_pending_changes()

        except KeyboardInterrupt:
            logger.info("Watcher interrupted by user")
            self.stop()

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
