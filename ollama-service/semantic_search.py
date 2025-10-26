"""
Semantic search using Smart Connections pre-computed embeddings + Ollama
"""
import json
import os
import re
import numpy as np
from pathlib import Path
import ollama


def load_smart_connections_embeddings(vault_path):
    """
    Load all Smart Connections embeddings from .smart-env folder

    Returns: dict of {file_path: embedding_vector}
    """
    smart_env_path = Path(vault_path) / '.smart-env' / 'multi'

    if not smart_env_path.exists():
        print(f"[WARNING] Smart Connections embeddings not found at {smart_env_path}")
        return {}

    embeddings = {}

    # Read all .ajson files
    for ajson_file in smart_env_path.glob('*.ajson'):
        try:
            with open(ajson_file, 'r', encoding='utf-8') as f:
                content = f.read()

                # Use regex to find the file path
                path_match = re.search(r'"path":"([^"]+)"', content)
                if not path_match:
                    continue

                file_path = path_match.group(1)

                # Try to find nomic-ai embedding vector (preferred, 768 dim)
                nomic_match = re.search(r'"nomic-ai/nomic-embed-text-v1.5":\{"vec":\[([^\]]+)\]', content)
                if nomic_match:
                    vec_str = nomic_match.group(1)
                    vec = [float(x) for x in vec_str.split(',')]
                    embeddings[file_path] = np.array(vec, dtype=np.float32)
                    continue

                # Fallback to bge-micro embedding (384 dim)
                bge_match = re.search(r'"TaylorAI/bge-micro-v2":\{"vec":\[([^\]]+)\]', content)
                if bge_match:
                    vec_str = bge_match.group(1)
                    vec = [float(x) for x in vec_str.split(',')]
                    embeddings[file_path] = np.array(vec, dtype=np.float32)

        except Exception as e:
            print(f"[WARNING] Error loading {ajson_file.name}: {str(e)[:80]}")
            continue

    print(f"[OK] Loaded {len(embeddings)} file embeddings from Smart Connections")
    return embeddings


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def find_relevant_files(question, vault_path, model='nomic-embed-text', top_k=15):
    """
    Find the most relevant files using semantic search

    Args:
        question: User's question
        vault_path: Path to the vault
        model: Ollama embedding model to use
        top_k: Number of top files to return

    Returns:
        List of tuples: [(file_path, similarity_score), ...]
    """
    # Load Smart Connections embeddings
    file_embeddings = load_smart_connections_embeddings(vault_path)

    if not file_embeddings:
        print("[WARNING] No Smart Connections embeddings found, falling back to random sampling")
        return []

    # Generate embedding for the question using Ollama
    try:
        print(f"[INFO] Generating embedding for question using {model}")
        response = ollama.embed(model=model, input=question)
        question_embedding = np.array(response['embeddings'][0], dtype=np.float32)
    except Exception as e:
        print(f"[ERROR] Failed to generate question embedding: {e}")
        return []

    # Calculate similarities
    similarities = []
    for file_path, file_embedding in file_embeddings.items():
        # Check if dimensions match
        if len(question_embedding) != len(file_embedding):
            continue

        similarity = cosine_similarity(question_embedding, file_embedding)
        similarities.append((file_path, similarity))

    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Return top K
    top_files = similarities[:top_k]

    print(f"[OK] Found {len(top_files)} relevant files")
    for i, (path, score) in enumerate(top_files[:5]):
        try:
            print(f"   {i+1}. {path} (score: {score:.3f})")
        except UnicodeEncodeError:
            # Handle Windows console encoding issues
            print(f"   {i+1}. [file {i+1}] (score: {score:.3f})")

    return top_files


# Test function
if __name__ == '__main__':
    # Test with Red-White vault
    test_vault = 'C:\\Users\\redpo\\repos\\Obsidian\\Multi-Vault\\Red-White.vault'
    test_question = "What are the characters?"

    # Use nomic-embed-text which matches Smart Connections embeddings
    results = find_relevant_files(test_question, test_vault, model='nomic-embed-text', top_k=10)

    print(f"\n\nTop 10 relevant files for '{test_question}':")
    for i, (path, score) in enumerate(results, 1):
        try:
            print(f"{i}. {path} ({score:.3f})")
        except UnicodeEncodeError:
            print(f"{i}. [file with special characters] ({score:.3f})")
