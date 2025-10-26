"""
Complete Flow Test - Index then Search

This tests the full flow: Index → Search → Verify
"""

import sys
sys.path.insert(0, '.')

from indexer import VaultIndexer
from hybrid_search import HybridSearch
from vector_store import VaultVectorStore

def test_complete_flow():
    """Test complete indexing and search flow"""
    print("=" * 60)
    print("Complete Flow Test: Index -> Search -> Verify")
    print("=" * 60)

    vault_path = r"C:\Users\redpo\repos\Obsidian\Multi-Vault\ThistleRidgeHall.vault"
    vault_name = "ThistleRidgeHall"
    db_path = "./chroma_db_complete"

    # Step 1: Initialize vector store
    print("\n1. Initializing vector store...")
    vector_store = VaultVectorStore(persist_directory=db_path)
    stats = vector_store.get_collection_stats(vault_name)
    print(f"   Current collection size: {stats['count']} documents")

    # Step 2: Index if empty
    if stats['count'] == 0:
        print("\n2. Collection empty - indexing vault...")
        indexer = VaultIndexer(
            vault_path=vault_path,
            vault_name=vault_name,
            vector_store=vector_store,
            batch_size=20
        )

        # Index only first 50 files for faster testing
        print("   Indexing first 50 files for quick testing...")
        files = indexer.metadata_extractor.get_vault_files()[:50]
        metadata_list = indexer.metadata_extractor.extract_batch(files)

        results = indexer.index_batch(metadata_list)
        print(f"   Indexed: {results['successful']}/{results['total']} files")

        # Verify
        stats = vector_store.get_collection_stats(vault_name)
        print(f"   New collection size: {stats['count']} documents")
    else:
        print(f"\n2. Collection already has {stats['count']} documents - skipping indexing")

    # Step 3: Test hybrid search
    print("\n3. Testing hybrid search...")
    hybrid_search = HybridSearch(vector_store)

    test_queries = [
        "what are all the artworks?",
        "files in Artworks folder",
        "artwork about apple trees"
    ]

    for query in test_queries:
        print(f"\n   Query: \"{query}\"")
        result = hybrid_search.search(vault_name, query, explain=False)
        print(f"   Type: {result['query_type']}")
        print(f"   Strategy: {result['search_strategy']}")
        print(f"   Results: {result['result_count']}")

        if result['results']:
            print(f"   Top 3:")
            for i, doc in enumerate(result['results'][:3], 1):
                print(f"   {i}. {doc['metadata']['file_path']}")

    # Step 4: The ultimate test
    print("\n" + "=" * 60)
    print("ULTIMATE TEST: List all artworks")
    print("=" * 60)

    result = hybrid_search.search(vault_name, "what are all the artworks?")

    artworks = [
        doc for doc in result['results']
        if doc['metadata'].get('folder') == 'Artworks'
    ]

    print(f"\nTotal artworks found: {len(artworks)}")
    print("\nArtwork files:")
    for i, doc in enumerate(artworks, 1):
        print(f"{i:2d}. {doc['metadata']['filename']}")

    if len(artworks) > 0:
        print("\n[SUCCESS] Found artworks using metadata filtering!")
    else:
        print("\n[ISSUE] No artworks found")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        test_complete_flow()
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
