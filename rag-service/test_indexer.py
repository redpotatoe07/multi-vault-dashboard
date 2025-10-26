"""
Test Indexer - Index entire vault

This test will index all 277 files from ThistleRidgeHall vault
"""

import sys
sys.path.insert(0, '.')

from indexer import VaultIndexer
from vector_store import VaultVectorStore
import time

def progress_callback(current, total):
    """Print progress"""
    percentage = (current / total) * 100
    print(f"   Progress: {current}/{total} ({percentage:.1f}%)", end='\r')

def test_indexer():
    """Test indexing entire vault"""
    print("=" * 60)
    print("Testing VaultIndexer - Full Vault Indexing")
    print("=" * 60)

    # Configuration
    vault_path = r"C:\Users\redpo\repos\Obsidian\Multi-Vault\ThistleRidgeHall.vault"
    vault_name = "ThistleRidgeHall"

    print(f"\nVault: {vault_name}")
    print(f"Path: {vault_path}")

    # Initialize vector store
    print("\n1. Initializing VaultVectorStore...")
    vector_store = VaultVectorStore(persist_directory="../chroma_db")
    print("   [OK] Vector store ready")

    # Check existing collection
    stats = vector_store.get_collection_stats(vault_name)
    print(f"   Current collection size: {stats['count']} documents")

    # Initialize indexer
    print("\n2. Initializing VaultIndexer...")
    indexer = VaultIndexer(
        vault_path=vault_path,
        vault_name=vault_name,
        vector_store=vector_store,
        batch_size=10  # Process 10 files at a time
    )
    print("   [OK] Indexer ready")

    # Get file count
    files = indexer.metadata_extractor.get_vault_files()
    print(f"   Files to index: {len(files)}")

    # Confirm before indexing
    print("\n" + "=" * 60)
    print("WARNING: This will index all files in the vault.")
    print(f"Total files: {len(files)}")
    print("Estimated time: ~10-15 minutes (depends on Ollama speed)")
    print("=" * 60)

    response = input("\nProceed with indexing? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Indexing cancelled.")
        return

    # Start indexing
    print("\n3. Starting full vault indexing...")
    print("   (This may take several minutes...)\n")

    start_time = time.time()

    # Index the vault
    results = indexer.index_vault(progress_callback=progress_callback)

    elapsed = time.time() - start_time

    # Print results
    print("\n\n" + "=" * 60)
    print("Indexing Results")
    print("=" * 60)
    print(f"Total files: {results['total']}")
    print(f"Successfully indexed: {results['successful']}")
    print(f"Failed: {results['failed']}")
    print(f"Elapsed time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    print(f"Speed: {results['docs_per_second']:.2f} docs/second")

    if results['errors']:
        print(f"\nErrors encountered: {len(results['errors'])}")
        for error in results['errors'][:5]:  # Show first 5 errors
            print(f"  - {error['file']}: {error['error']}")
        if len(results['errors']) > 5:
            print(f"  ... and {len(results['errors']) - 5} more errors")

    # Verify final collection size
    print("\n4. Verifying collection...")
    final_stats = vector_store.get_collection_stats(vault_name)
    print(f"   Final collection size: {final_stats['count']} documents")

    # Test a quick search
    print("\n5. Testing quick search...")
    import ollama

    query = "artwork about apple trees"
    print(f"   Query: '{query}'")

    query_embedding = ollama.embeddings(
        model='nomic-embed-text',
        prompt=query
    )['embedding']

    search_results = vector_store.query(
        collection_name=vault_name,
        query_embeddings=[query_embedding],
        n_results=3
    )

    print(f"   Top 3 results:")
    for i, doc_id in enumerate(search_results['ids'][0], 1):
        metadata = search_results['metadatas'][0][i-1]
        distance = search_results['distances'][0][i-1]
        print(f"   {i}. {metadata['file_path']} (distance: {distance:.2f})")

    print("\n" + "=" * 60)
    print("[SUCCESS] Full vault indexing complete!")
    print("=" * 60)
    print(f"\nThe '{vault_name}' vault is now fully indexed and searchable.")
    print(f"Total documents: {final_stats['count']}")

if __name__ == "__main__":
    try:
        test_indexer()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Indexing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
