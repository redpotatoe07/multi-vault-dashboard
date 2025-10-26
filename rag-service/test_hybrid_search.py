"""
Test HybridSearch - The moment of truth!

This test will verify that we can correctly answer "list all artworks"
and return ALL 48 artworks, not just 15.
"""

import sys
sys.path.insert(0, '.')

from hybrid_search import HybridSearch
from vector_store import VaultVectorStore
from query_router import QueryRouter
import json

def test_hybrid_search():
    """Test hybrid search with various query types"""
    print("=" * 60)
    print("Testing HybridSearch - The Moment of Truth!")
    print("=" * 60)

    vault_name = "ThistleRidgeHall"

    # Initialize components
    print("\n1. Initializing components...")
    vector_store = VaultVectorStore(persist_directory="../chroma_db")
    hybrid_search = HybridSearch(vector_store)
    print("   [OK] Components ready")

    # Verify collection size
    stats = vector_store.get_collection_stats(vault_name)
    print(f"   Collection size: {stats['count']} documents")

    # Test queries
    test_queries = [
        {
            "query": "what are all the artworks?",
            "expected_type": "LIST_ALL",
            "description": "The big test - list ALL artworks"
        },
        {
            "query": "list all the characters",
            "expected_type": "LIST_ALL",
            "description": "List all characters"
        },
        {
            "query": "files in the Artworks folder",
            "expected_type": "FILTER",
            "description": "Filter by folder"
        },
        {
            "query": "artwork about apple trees",
            "expected_type": "SEARCH",
            "description": "Semantic search for specific artwork"
        },
        {
            "query": "who is Cerys ferch Rhys",
            "expected_type": "SPECIFIC",
            "description": "Specific entity lookup"
        }
    ]

    print("\n" + "=" * 60)
    print("Running Test Queries")
    print("=" * 60)

    for i, test in enumerate(test_queries, 1):
        query = test["query"]
        expected_type = test["expected_type"]
        description = test["description"]

        print(f"\n{i}. {description}")
        print(f"   Query: \"{query}\"")
        print(f"   Expected type: {expected_type}")

        # Perform search
        result = hybrid_search.search(
            vault_name=vault_name,
            query=query,
            explain=True
        )

        # Display results
        print(f"   Detected type: {result['query_type'].upper()}")
        print(f"   Strategy: {result['search_strategy']}")
        print(f"   Results: {result['result_count']} documents")

        # Check if classification matches expectation
        if result['query_type'].upper() == expected_type:
            print("   [OK] Query type correctly identified")
        else:
            print(f"   [WARNING] Expected {expected_type}, got {result['query_type'].upper()}")

        # Show top results
        if result['results']:
            print(f"\n   Top results:")
            for j, doc in enumerate(result['results'][:5], 1):
                metadata = doc['metadata']
                score = doc.get('score', 'N/A')
                print(f"   {j}. {metadata['file_path']} (score: {score:.3f})")

            # For LIST_ALL queries, show full count
            if result['query_type'] == 'list_all':
                print(f"\n   Total found: {result['result_count']} documents")

                # Group by folder to verify
                folders = {}
                for doc in result['results']:
                    folder = doc['metadata'].get('folder', 'Unknown')
                    folders[folder] = folders.get(folder, 0) + 1

                print(f"   Breakdown by folder:")
                for folder, count in sorted(folders.items()):
                    print(f"   - {folder}: {count} files")

    # The ULTIMATE TEST - List all artworks
    print("\n\n" + "=" * 60)
    print("THE ULTIMATE TEST: List All Artworks")
    print("=" * 60)

    ultimate_query = "what are all the artworks?"
    print(f"\nQuery: \"{ultimate_query}\"")
    print("\nThis is the query that failed with semantic search,")
    print("only returning 15 out of 48 artworks.")
    print("\nLet's see if hybrid search can solve it...\n")

    result = hybrid_search.search(
        vault_name=vault_name,
        query=ultimate_query,
        explain=True
    )

    print(f"Query type: {result['query_type']}")
    print(f"Strategy: {result['search_strategy']}")
    print(f"Total results: {result['result_count']}")

    # Count artworks in the Artworks folder
    artworks_folder_count = sum(
        1 for doc in result['results']
        if doc['metadata'].get('folder') == 'Artworks'
    )

    print(f"\nDocuments in 'Artworks' folder: {artworks_folder_count}")

    if artworks_folder_count >= 48:
        print("\n" + "=" * 60)
        print("[SUCCESS] Found all artworks! Problem SOLVED!")
        print("=" * 60)
    elif artworks_folder_count > 15:
        print(f"\n[PROGRESS] Found {artworks_folder_count} artworks (better than 15!)")
    else:
        print(f"\n[ISSUE] Only found {artworks_folder_count} artworks")

    # Show all artwork filenames
    if result['results']:
        print("\nAll artworks found:")
        artwork_results = [
            doc for doc in result['results']
            if doc['metadata'].get('folder') == 'Artworks'
        ]

        for i, doc in enumerate(artwork_results, 1):
            filename = doc['metadata']['filename']
            print(f"{i:3d}. {filename}")

    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_hybrid_search()
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
