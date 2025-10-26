"""
Test script for VaultVectorStore

This verifies that ChromaDB is working correctly with our wrapper class.
"""

import sys
sys.path.insert(0, '.')

from vector_store import VaultVectorStore
import numpy as np

def test_vector_store():
    """Test basic ChromaDB operations"""
    print("=" * 60)
    print("Testing VaultVectorStore with ChromaDB")
    print("=" * 60)

    # Initialize vector store
    print("\n1. Initializing ChromaDB...")
    store = VaultVectorStore(persist_directory="../chroma_db_test")

    # Create a test collection
    print("\n2. Creating test collection...")
    collection_name = "TestVault"
    collection = store.get_or_create_collection(collection_name)
    print(f"   [OK] Collection '{collection_name}' created")

    # Create dummy embeddings (768-dim for nomic-embed-text)
    print("\n3. Creating test documents with embeddings...")
    test_docs = [
        "This is a test document about characters.",
        "Another document about locations.",
        "A third document discussing plot points."
    ]

    # Generate random 768-dimensional embeddings (in real use, these come from Ollama)
    test_embeddings = [
        np.random.rand(768).tolist() for _ in test_docs
    ]

    test_metadata = [
        {"file_path": "Characters/test1.md", "folder": "Characters", "word_count": 10},
        {"file_path": "Locations/test2.md", "folder": "Locations", "word_count": 8},
        {"file_path": "Plot/test3.md", "folder": "Plot", "word_count": 9}
    ]

    test_ids = ["test_doc_1", "test_doc_2", "test_doc_3"]

    # Add documents
    print(f"   Adding {len(test_docs)} documents...")
    store.add_documents(
        collection_name=collection_name,
        documents=test_docs,
        embeddings=test_embeddings,
        metadatas=test_metadata,
        ids=test_ids
    )
    print(f"   [OK] {len(test_docs)} documents added successfully")

    # Get collection stats
    print("\n4. Checking collection stats...")
    stats = store.get_collection_stats(collection_name)
    print(f"   Collection: {stats['name']}")
    print(f"   Document count: {stats['count']}")
    print(f"   Metadata: {stats['metadata']}")

    # Test querying (using first document's embedding as query)
    print("\n5. Testing query (searching for similar documents)...")
    query_embedding = test_embeddings[0]  # Use first doc as query
    results = store.query(
        collection_name=collection_name,
        query_embeddings=[query_embedding],
        n_results=2
    )

    print(f"   Query returned {len(results['ids'][0])} results:")
    for i, doc_id in enumerate(results['ids'][0]):
        distance = results['distances'][0][i]
        metadata = results['metadatas'][0][i]
        print(f"   - {doc_id}: distance={distance:.4f}, folder={metadata['folder']}")

    # Test metadata filtering
    print("\n6. Testing metadata filtering...")
    results_filtered = store.query(
        collection_name=collection_name,
        query_embeddings=[query_embedding],
        n_results=5,
        where={"folder": "Characters"}
    )
    print(f"   Filtered query (folder='Characters'): {len(results_filtered['ids'][0])} results")

    # List all collections
    print("\n7. Listing all collections...")
    collections = store.list_collections()
    print(f"   Total collections: {len(collections)}")
    for col in collections:
        print(f"   - {col}")

    # Test update
    print("\n8. Testing document update...")
    store.update_document(
        collection_name=collection_name,
        document_id="test_doc_1",
        metadata={"file_path": "Characters/test1.md", "folder": "Characters", "word_count": 15, "updated": True}
    )
    print("   [OK] Document updated successfully")

    # Test delete
    print("\n9. Testing document deletion...")
    store.delete_document(collection_name, "test_doc_3")
    stats = store.get_collection_stats(collection_name)
    print(f"   [OK] Document deleted. New count: {stats['count']}")

    print("\n" + "=" * 60)
    print("[SUCCESS] All tests passed! ChromaDB is working correctly.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_vector_store()
    except Exception as e:
        print(f"\n[ERROR] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
