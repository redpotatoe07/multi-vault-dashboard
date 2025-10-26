"""
Full Indexing Test - Combine VaultVectorStore + MetadataExtractor + Ollama Embeddings

This test demonstrates the complete flow:
1. Extract metadata from a vault file
2. Generate embeddings using Ollama (nomic-embed-text)
3. Store in ChromaDB
4. Query to retrieve the document
"""

import sys
sys.path.insert(0, '.')

from vector_store import VaultVectorStore
from metadata_extractor import MetadataExtractor
import ollama
import json

def test_full_indexing():
    """Test complete indexing pipeline"""
    print("=" * 60)
    print("Testing Full Indexing Pipeline")
    print("=" * 60)

    # Configuration
    vault_path = r"C:\Users\redpo\repos\Obsidian\Multi-Vault\ThistleRidgeHall.vault"
    vault_name = "ThistleRidgeHall"

    # Step 1: Extract metadata
    print("\n1. Extracting metadata from vault file...")
    extractor = MetadataExtractor(vault_path)
    files = extractor.get_vault_files()

    if len(files) == 0:
        print("   [ERROR] No files found in vault!")
        return

    # Use first file as test
    test_file = files[0]
    print(f"   Test file: {test_file}")

    metadata = extractor.extract(test_file)
    print(f"   [OK] Metadata extracted")
    print(f"   - File: {metadata['file_path']}")
    print(f"   - Folder: {metadata['folder']}")
    print(f"   - Word count: {metadata['word_count']}")

    # Step 2: Generate embedding using Ollama
    print("\n2. Generating embedding with Ollama (nomic-embed-text)...")

    # Prepare text for embedding (combine filename, folder, tags, and content)
    embedding_text = f"""
    Title: {metadata['filename'].replace('.md', '')}
    Folder: {metadata['folder']}
    Tags: {', '.join(metadata['all_tags'])}
    Content: {metadata['content'][:500]}
    """.strip()

    try:
        response = ollama.embeddings(
            model='nomic-embed-text',
            prompt=embedding_text
        )
        embedding = response['embedding']
        print(f"   [OK] Embedding generated ({len(embedding)} dimensions)")

    except Exception as e:
        print(f"   [ERROR] Failed to generate embedding: {e}")
        print("   Make sure Ollama is running and nomic-embed-text model is available")
        return

    # Step 3: Store in ChromaDB
    print("\n3. Storing document in ChromaDB...")
    store = VaultVectorStore(persist_directory="../chroma_db")

    # Prepare metadata for ChromaDB (convert complex types to strings)
    chroma_metadata = {
        "file_path": metadata['file_path'],
        "filename": metadata['filename'],
        "folder": metadata['folder'],
        "word_count": metadata['word_count'],
        "created": metadata['created'],
        "modified": metadata['modified'],
        "tags": json.dumps(metadata['all_tags']),  # Store as JSON string
        "wikilinks_count": metadata['wikilinks_count'],
        "heading_count": metadata['heading_count']
    }

    # Add to ChromaDB
    store.add_documents(
        collection_name=vault_name,
        documents=[metadata['content']],
        embeddings=[embedding],
        metadatas=[chroma_metadata],
        ids=[metadata['file_id']]
    )

    print(f"   [OK] Document added to collection '{vault_name}'")

    # Step 4: Verify storage
    print("\n4. Verifying document was stored...")
    stats = store.get_collection_stats(vault_name)
    print(f"   Collection: {stats['name']}")
    print(f"   Total documents: {stats['count']}")

    # Step 5: Test querying (search for similar documents)
    print("\n5. Testing semantic search...")

    # Query: "artwork about apple trees"
    query_text = "artwork about apple trees"
    print(f"   Query: '{query_text}'")

    # Generate query embedding
    query_response = ollama.embeddings(
        model='nomic-embed-text',
        prompt=query_text
    )
    query_embedding = query_response['embedding']

    # Search ChromaDB
    results = store.query(
        collection_name=vault_name,
        query_embeddings=[query_embedding],
        n_results=1
    )

    if results['ids'][0]:
        result_id = results['ids'][0][0]
        result_distance = results['distances'][0][0]
        result_metadata = results['metadatas'][0][0]

        print(f"   [OK] Found match!")
        print(f"   - File: {result_metadata['file_path']}")
        print(f"   - Folder: {result_metadata['folder']}")
        print(f"   - Distance: {result_distance:.4f}")
        print(f"   - Tags: {result_metadata['tags']}")

    # Step 6: Test metadata filtering
    print("\n6. Testing metadata filtering...")
    results_filtered = store.query(
        collection_name=vault_name,
        query_embeddings=[query_embedding],
        n_results=5,
        where={"folder": metadata['folder']}
    )

    print(f"   Filter: folder='{metadata['folder']}'")
    print(f"   Results: {len(results_filtered['ids'][0])} documents")

    print("\n" + "=" * 60)
    print("[SUCCESS] Full indexing pipeline works!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Index all vault files (277 files)")
    print("2. Build hybrid search (semantic + keyword + metadata)")
    print("3. Add file watcher for real-time updates")
    print("4. Create Flask API endpoints")

if __name__ == "__main__":
    try:
        test_full_indexing()
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
