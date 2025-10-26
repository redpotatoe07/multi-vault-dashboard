# Phase 3B: Full RAG System Implementation Plan

**Version**: 0.3.0
**Status**: 📋 Planning
**Estimated Duration**: 3-5 days
**Date Created**: 2025-10-17

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Why Full RAG System?](#why-full-rag-system)
3. [Architecture Overview](#architecture-overview)
4. [Technology Stack](#technology-stack)
5. [Implementation Steps](#implementation-steps)
6. [File Structure](#file-structure)
7. [API Design](#api-design)
8. [Database Schema](#database-schema)
9. [Testing Strategy](#testing-strategy)
10. [Migration Path](#migration-path)
11. [Future Enhancements](#future-enhancements)

---

## Executive Summary

**Goal**: Build a production-ready RAG (Retrieval-Augmented Generation) system that provides:
- Accurate file retrieval (semantic + keyword + metadata)
- Foundation for write operations (tasks, updates)
- Scalability to 1000+ files per vault
- Real-time indexing with file watchers
- Robust query understanding

**What Gets Built**:
1. ChromaDB vector database for embeddings
2. Python RAG service with hybrid search
3. Metadata extraction and indexing
4. File watcher for auto-updates
5. Write operations API (for future dashboard integrations)

**What Gets Better**:
- ✅ "What are all the artworks?" → Returns ALL artworks, not just similar ones
- ✅ "Show characters from Chapter 5" → Can filter by metadata
- ✅ "List files modified this week" → Can query by date
- ✅ Foundation for "Add task to vault" → Write API ready

---

## Why Full RAG System?

### Current Smart Connections Limitations

| Problem | Impact | Example |
|---------|--------|---------|
| **Semantic similarity only** | Misses exhaustive queries | "List all artworks" → Found 1/48 files |
| **No metadata filtering** | Can't filter by folder/date/tags | "Show recent files" → Impossible |
| **Fragile thresholds** | Requires constant tuning | 0.45 vs 0.50 vs 0.55 confusion |
| **Read-only dependency** | Can't build write features | No task creation, no updates |
| **No query understanding** | Treats all queries the same | "All X" same as "Tell me about X" |

### Full RAG Benefits

| Feature | Benefit | Use Case |
|---------|---------|----------|
| **Hybrid search** | Semantic + keyword + metadata | "Artworks about landscapes in 2024" |
| **Metadata extraction** | Query by folder/tags/dates | "Files in Characters folder" |
| **Query classification** | Different strategies per query type | List all vs Find similar |
| **Write operations** | Build interactive dashboard | Add tasks, update files |
| **File watcher** | Real-time updates | Index new files automatically |
| **Scalable** | Handle 1000+ files | Multi-vault with large collections |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Browser (React + Markdown)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/SSE
┌────────────────────────────▼────────────────────────────────────┐
│                   Node.js Express Server                        │
│  - Routes requests to Python services                           │
│  - Handles SSE streaming                                        │
│  - Static file serving                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP
         ┌───────────────────┴──────────────────┐
         │                                      │
┌────────▼──────────┐              ┌───────────▼──────────┐
│  Python RAG       │              │  Python Write API    │
│  Service          │              │  (Future)            │
│                   │              │                      │
│  - Query Router   │              │  - Task Creator      │
│  - Hybrid Search  │              │  - File Updater      │
│  - Embeddings     │              │  - YAML Parser       │
│  - Ollama Chat    │              │  - Vault Writer      │
└────────┬──────────┘              └───────────┬──────────┘
         │                                     │
         ├─────────────────────────────────────┘
         │
┌────────▼───────────────────────────────────────────────────────┐
│                       ChromaDB                                  │
│  Collections (per vault):                                       │
│    - Document embeddings (768-dim nomic)                        │
│    - Metadata: {file_path, folder, tags, modified, size}       │
│    - Full text (for keyword search)                             │
└────────┬───────────────────────────────────────────────────────┘
         │
┌────────▼───────────────────────────────────────────────────────┐
│                  File System Watcher                            │
│  - Watches vault directories                                    │
│  - Auto-indexes new/modified files                              │
│  - Removes deleted files from ChromaDB                          │
└────────┬───────────────────────────────────────────────────────┘
         │
┌────────▼───────────────────────────────────────────────────────┐
│              Obsidian Vaults (File System)                      │
│  C:\Users\redpo\repos\Obsidian\Multi-Vault\                    │
│    ├── Red-White.vault/                                         │
│    ├── ThistleRidgeHall.vault/                                  │
│    └── Study.vault/                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Core Technologies

| Component | Technology | Why? |
|-----------|-----------|------|
| **Vector DB** | ChromaDB | Lightweight, embeds in Python, perfect for local use |
| **Embeddings** | nomic-embed-text (Ollama) | 768-dim, same as Smart Connections, local inference |
| **Python Service** | Flask | Already using it, easy to extend |
| **File Watcher** | watchdog | Cross-platform, reliable, Python-native |
| **YAML Parser** | python-frontmatter | Parse Obsidian frontmatter |
| **Markdown Parser** | python-markdown | Extract content sections |

### New Dependencies

```txt
# Add to ollama-service/requirements.txt
chromadb==0.4.18          # Vector database
watchdog==3.0.0           # File system watcher
python-frontmatter==1.0.1 # YAML frontmatter parser
python-markdown==3.5.1    # Markdown parsing
sentence-transformers==2.2.2  # For fallback embeddings
```

---

## Implementation Steps

### Step 1: Setup ChromaDB (Day 1, 2-3 hours)

**Goal**: Get ChromaDB running with basic indexing

**Tasks**:
1. Install ChromaDB and dependencies
2. Create `rag_service/` directory structure
3. Write `vector_store.py` - ChromaDB wrapper
4. Write `indexer.py` - Index vault files
5. Test basic storage and retrieval

**Deliverables**:
- `rag_service/vector_store.py` - ChromaDB interface
- `rag_service/indexer.py` - File indexing logic
- `rag_service/metadata_extractor.py` - Parse YAML/markdown
- Test script that indexes sample vault

**Code Preview**:
```python
# rag_service/vector_store.py
import chromadb
from chromadb.config import Settings

class VaultVectorStore:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))

    def get_or_create_collection(self, vault_name):
        """Get or create collection for a vault"""
        return self.client.get_or_create_collection(
            name=vault_name.replace(".", "_"),
            metadata={"description": f"Documents from {vault_name}"}
        )

    def add_document(self, collection, doc_id, text, embedding, metadata):
        """Add a document to the collection"""
        collection.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata]
        )
```

---

### Step 2: Metadata Extraction (Day 1, 2-3 hours)

**Goal**: Extract rich metadata from Obsidian files

**Tasks**:
1. Parse YAML frontmatter (tags, dates, custom fields)
2. Extract folder structure
3. Get file stats (size, modified date)
4. Parse markdown sections (headings)
5. Handle special Obsidian syntax (wikilinks, embeds)

**Deliverables**:
- `rag_service/metadata_extractor.py`

**Metadata Schema**:
```python
{
    "file_path": "Characters/Captain Novák.md",
    "folder": "Characters",
    "filename": "Captain Novák.md",
    "tags": ["character", "military", "protagonist"],
    "created": "2024-01-15T10:30:00",
    "modified": "2024-10-15T14:20:00",
    "size_bytes": 5432,
    "yaml_frontmatter": {
        "title": "Captain Václav Novák",
        "type": "character",
        "status": "active"
    },
    "headings": ["Overview", "Background", "Personality"],
    "word_count": 842,
    "has_wikilinks": true,
    "linked_files": ["Běla Novák.md", "Red Legion.md"]
}
```

**Code Preview**:
```python
# rag_service/metadata_extractor.py
import frontmatter
import os
from pathlib import Path
from datetime import datetime

class MetadataExtractor:
    def extract(self, file_path):
        """Extract all metadata from a markdown file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # Get file stats
        stat = os.stat(file_path)
        path_obj = Path(file_path)

        metadata = {
            "file_path": str(path_obj.relative_to(vault_root)),
            "folder": str(path_obj.parent.name),
            "filename": path_obj.name,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "size_bytes": stat.st_size,
            "yaml_frontmatter": dict(post.metadata),
            "content": post.content,
            "word_count": len(post.content.split())
        }

        # Extract tags
        tags = post.metadata.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        metadata['tags'] = tags

        return metadata
```

---

### Step 3: Hybrid Search System (Day 2, 4-5 hours)

**Goal**: Implement intelligent query routing and hybrid search

**Tasks**:
1. Create query classifier (list all vs find similar vs filter)
2. Implement semantic search (vector similarity)
3. Implement keyword search (full-text)
4. Implement metadata filters (folder, tags, date)
5. Combine results with ranking

**Deliverables**:
- `rag_service/query_router.py` - Classify queries
- `rag_service/hybrid_search.py` - Search logic
- `rag_service/ranker.py` - Result ranking

**Query Types**:
```python
class QueryType(Enum):
    LIST_ALL = "list_all"        # "What are all the artworks?"
    FIND_SIMILAR = "find_similar" # "Files like this one"
    FILTER = "filter"            # "Files in Characters folder"
    SEARCH = "search"            # "Files about dragons"
    SPECIFIC = "specific"        # "Who is Captain Novák?"
```

**Code Preview**:
```python
# rag_service/query_router.py
import re
from enum import Enum

class QueryRouter:
    def classify(self, question):
        """Classify the query type"""
        lower = question.lower()

        # Pattern matching for query types
        list_all_patterns = [
            r'\b(all|list|show|what are|give me)\b.*\b(file|artwork|character|location)s?\b',
            r'\bshow me (all|everything)\b'
        ]

        for pattern in list_all_patterns:
            if re.search(pattern, lower):
                return {
                    'type': QueryType.LIST_ALL,
                    'strategy': 'metadata_filter',
                    'use_semantic': False
                }

        # ... more patterns

        return {
            'type': QueryType.SEARCH,
            'strategy': 'hybrid',
            'use_semantic': True
        }

# rag_service/hybrid_search.py
class HybridSearch:
    def search(self, collection, query, query_type, top_k=20):
        """Perform hybrid search"""

        if query_type['type'] == QueryType.LIST_ALL:
            # Use metadata filtering only
            results = collection.get(
                where={"folder": {"$contains": "Artworks"}}
            )
            return results

        elif query_type['strategy'] == 'hybrid':
            # Combine semantic + keyword
            semantic_results = collection.query(
                query_embeddings=[self.embed(query)],
                n_results=top_k
            )

            keyword_results = collection.query(
                query_texts=[query],
                n_results=top_k
            )

            # Merge and rank
            return self.merge_results(semantic_results, keyword_results)
```

---

### Step 4: File Watcher (Day 2, 2-3 hours)

**Goal**: Automatically index new/modified files

**Tasks**:
1. Setup watchdog file system observer
2. Handle file created events
3. Handle file modified events
4. Handle file deleted events
5. Debounce rapid changes

**Deliverables**:
- `rag_service/file_watcher.py`

**Code Preview**:
```python
# rag_service/file_watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class VaultWatcher(FileSystemEventHandler):
    def __init__(self, indexer, vault_path):
        self.indexer = indexer
        self.vault_path = vault_path
        self.debounce_time = {}

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.md'):
            return

        print(f"[INFO] New file detected: {event.src_path}")
        self.indexer.index_file(event.src_path)

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.md'):
            return

        # Debounce - wait 2 seconds after last change
        current_time = time.time()
        last_time = self.debounce_time.get(event.src_path, 0)

        if current_time - last_time < 2:
            return

        self.debounce_time[event.src_path] = current_time
        print(f"[INFO] File modified: {event.src_path}")
        self.indexer.reindex_file(event.src_path)

    def on_deleted(self, event):
        if event.is_directory or not event.src_path.endswith('.md'):
            return

        print(f"[INFO] File deleted: {event.src_path}")
        self.indexer.remove_file(event.src_path)

def start_watching(vault_path, indexer):
    """Start watching a vault directory"""
    event_handler = VaultWatcher(indexer, vault_path)
    observer = Observer()
    observer.schedule(event_handler, vault_path, recursive=True)
    observer.start()
    return observer
```

---

### Step 5: RAG Service API (Day 3, 4-5 hours)

**Goal**: Create Flask API for RAG operations

**Tasks**:
1. Create new Flask app `rag_service/app.py`
2. Add `/index-vault` endpoint (trigger indexing)
3. Add `/search` endpoint (hybrid search)
4. Add `/get-document` endpoint (retrieve specific file)
5. Add `/stats` endpoint (collection statistics)

**Deliverables**:
- `rag_service/app.py` - Flask API
- Integration with existing ollama-service

**API Endpoints**:

```python
# rag_service/app.py
from flask import Flask, request, jsonify
from vector_store import VaultVectorStore
from indexer import VaultIndexer
from hybrid_search import HybridSearch
from query_router import QueryRouter

app = Flask(__name__)
vector_store = VaultVectorStore()
indexer = VaultIndexer(vector_store)
searcher = HybridSearch()
router = QueryRouter()

@app.route('/index-vault', methods=['POST'])
def index_vault():
    """
    Index an entire vault

    Body: {
        "vault_name": "Red-White",
        "vault_path": "C:\\...\\Red-White.vault"
    }
    """
    data = request.json
    vault_name = data.get('vault_name')
    vault_path = data.get('vault_path')

    # Index all files
    result = indexer.index_vault(vault_name, vault_path)

    return jsonify({
        'success': True,
        'files_indexed': result['count'],
        'duration_seconds': result['duration']
    })

@app.route('/search', methods=['POST'])
def search():
    """
    Search for documents

    Body: {
        "vault_name": "Red-White",
        "question": "What are all the characters?",
        "top_k": 20
    }
    """
    data = request.json
    vault_name = data.get('vault_name')
    question = data.get('question')
    top_k = data.get('top_k', 20)

    # Classify query
    query_type = router.classify(question)

    # Get collection
    collection = vector_store.get_or_create_collection(vault_name)

    # Search
    results = searcher.search(collection, question, query_type, top_k)

    return jsonify({
        'success': True,
        'query_type': query_type['type'].value,
        'results': results,
        'count': len(results)
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Get statistics for all vaults"""
    collections = vector_store.client.list_collections()

    stats = {}
    for collection in collections:
        stats[collection.name] = {
            'document_count': collection.count(),
            'metadata': collection.metadata
        }

    return jsonify({
        'success': True,
        'vaults': stats
    })
```

---

### Step 6: Integration with Node.js (Day 3, 2-3 hours)

**Goal**: Update Node.js server to use RAG service

**Tasks**:
1. Update `server.js` to call RAG service instead of semantic search
2. Add indexing trigger on server startup
3. Update frontend to show indexing status
4. Test end-to-end flow

**Deliverables**:
- Updated `server.js`
- Updated `public/app.js`

**Code Changes**:
```javascript
// server.js
const RAG_SERVICE_URL = 'http://localhost:5001';

// New endpoint: Trigger indexing
app.post('/api/rag/index-vault', async (req, res) => {
  const { vault } = req.body;

  const vaultConfig = scanner.vaults.find(v => v.name === vault);
  const vaultPath = path.join(VAULT_ROOT, vaultConfig.path);

  const response = await fetch(`${RAG_SERVICE_URL}/index-vault`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vault_name: vault,
      vault_path: vaultPath
    })
  });

  const data = await response.json();
  res.json(data);
});

// Updated: Ask endpoint uses RAG search
app.post('/api/ollama/ask', async (req, res) => {
  const { question, vault } = req.body;

  // Use RAG service for file retrieval
  const searchResponse = await fetch(`${RAG_SERVICE_URL}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vault_name: vault,
      question: question,
      top_k: 30
    })
  });

  const searchData = await searchResponse.json();

  // Build file content from RAG results
  const fileContent = searchData.results.map(doc =>
    `--- FILE: ${doc.metadata.filename} ---\n${doc.content}\n\n`
  ).join('');

  // Continue with Ollama chat as before...
});
```

---

### Step 7: Testing & Optimization (Day 4, Full day)

**Goal**: Ensure system works reliably

**Tasks**:
1. Test indexing performance (1000+ files)
2. Test query accuracy (all query types)
3. Test file watcher (add/modify/delete files)
4. Optimize embedding generation (batch processing)
5. Add caching for frequently accessed documents
6. Performance profiling and optimization

**Test Cases**:
```python
# tests/test_rag_system.py

def test_list_all_artworks():
    """Should return ALL artwork files"""
    results = search("What are all the artworks?", "ThistleRidgeHall")
    assert len(results) == 48  # All artworks
    assert all("Artworks/" in r['metadata']['file_path'] for r in results)

def test_find_specific_character():
    """Should find specific character file"""
    results = search("Who is Captain Novák?", "Red-White")
    assert len(results) > 0
    assert "Captain Václav Novák.md" in results[0]['metadata']['filename']

def test_filter_by_folder():
    """Should filter files by folder"""
    results = search("Files in Characters folder", "Red-White")
    assert all("Characters/" in r['metadata']['file_path'] for r in results)

def test_filter_by_date():
    """Should find recently modified files"""
    results = search("Files modified this week", "Red-White")
    # Check dates are within last 7 days

def test_semantic_search():
    """Should find semantically similar files"""
    results = search("military leaders", "Red-White")
    # Should include Captain Novák even if "military" not in text
```

---

### Step 8: Write Operations Foundation (Day 5, 4-5 hours)

**Goal**: Build API for future write operations

**Tasks**:
1. Create `vault_writer.py` - Safe file writing
2. Add `/create-task` endpoint
3. Add `/update-file` endpoint
4. Add file locking for concurrent access
5. Validate YAML frontmatter before writing

**Deliverables**:
- `rag_service/vault_writer.py`
- Write API endpoints in `rag_service/app.py`

**Code Preview**:
```python
# rag_service/vault_writer.py
import os
import frontmatter
from pathlib import Path
from datetime import datetime

class VaultWriter:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)

    def create_task(self, title, content, folder="Tasks"):
        """
        Create a new task file in the vault

        Args:
            title: Task title
            content: Task description
            folder: Subfolder to create task in

        Returns:
            Path to created file
        """
        # Create safe filename
        filename = self._safe_filename(title)
        filepath = self.vault_path / folder / f"{filename}.md"

        # Ensure folder exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Create frontmatter
        post = frontmatter.Post(content)
        post.metadata = {
            'title': title,
            'created': datetime.now().isoformat(),
            'status': 'pending',
            'tags': ['task', 'dashboard-created']
        }

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        return str(filepath)

    def update_frontmatter(self, filepath, updates):
        """
        Update YAML frontmatter of a file

        Args:
            filepath: Path to file
            updates: Dict of frontmatter fields to update
        """
        full_path = self.vault_path / filepath

        with open(full_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # Update metadata
        post.metadata.update(updates)
        post.metadata['modified'] = datetime.now().isoformat()

        # Write back
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

    def _safe_filename(self, title):
        """Convert title to safe filename"""
        # Remove invalid characters
        safe = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_'))
        return safe.strip().replace(' ', '-')

# API endpoint
@app.route('/create-task', methods=['POST'])
def create_task():
    """
    Create a task in the vault

    Body: {
        "vault_name": "Red-White",
        "vault_path": "C:\\...\\Red-White.vault",
        "title": "Review Chapter 5",
        "content": "Need to review and revise chapter 5 draft",
        "folder": "Tasks"
    }
    """
    data = request.json
    vault_path = data.get('vault_path')
    title = data.get('title')
    content = data.get('content')
    folder = data.get('folder', 'Tasks')

    writer = VaultWriter(vault_path)
    filepath = writer.create_task(title, content, folder)

    # Also index the new file
    indexer.index_file(filepath)

    return jsonify({
        'success': True,
        'filepath': filepath
    })
```

---

### Step 9: Documentation (Day 5, 2-3 hours)

**Goal**: Document the new system

**Tasks**:
1. Update README.md with RAG system
2. Create RAG_ARCHITECTURE.md
3. Update SETUP.md with ChromaDB setup
4. Create API_REFERENCE.md
5. Add code comments and docstrings

**Deliverables**:
- Updated documentation
- API reference
- Architecture diagrams

---

## File Structure

```
multi-vault-dashboard/
├── ollama-service/              # Existing Ollama service
│   ├── app.py                   # Chat endpoint
│   ├── semantic_search.py       # OLD - To be deprecated
│   └── requirements.txt
│
├── rag-service/                 # NEW - RAG service
│   ├── app.py                   # Flask API (search, index, write)
│   ├── vector_store.py          # ChromaDB wrapper
│   ├── indexer.py               # Index vault files
│   ├── metadata_extractor.py   # Parse YAML/markdown
│   ├── hybrid_search.py         # Search logic
│   ├── query_router.py          # Query classification
│   ├── ranker.py                # Result ranking
│   ├── file_watcher.py          # Watch for file changes
│   ├── vault_writer.py          # Write operations
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # RAG service docs
│
├── chroma_db/                   # NEW - Vector database storage
│   ├── chroma.sqlite3           # ChromaDB database
│   └── [collection folders]
│
├── server.js                    # Node.js server (UPDATED)
├── public/
│   └── app.js                   # Frontend (UPDATED)
│
├── docs/                        # NEW - Documentation
│   ├── RAG_ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   └── QUERY_EXAMPLES.md
│
├── tests/                       # NEW - Test suite
│   ├── test_indexer.py
│   ├── test_search.py
│   ├── test_query_router.py
│   └── test_write_operations.py
│
├── PHASE_3B_IMPLEMENTATION_PLAN.md  # This file
├── IMPLEMENTATION_SUMMARY.md        # Updated with Phase 3B
├── CHANGELOG.md                     # Updated with v0.3.0
└── README.md                        # Updated
```

---

## API Design

### RAG Service API (Port 5001)

#### POST /index-vault
Index an entire vault into ChromaDB.

**Request**:
```json
{
  "vault_name": "Red-White",
  "vault_path": "C:\\Users\\...\\Red-White.vault",
  "force_reindex": false
}
```

**Response**:
```json
{
  "success": true,
  "files_indexed": 127,
  "duration_seconds": 45.3,
  "embeddings_generated": 127
}
```

---

#### POST /search
Search for documents using hybrid search.

**Request**:
```json
{
  "vault_name": "Red-White",
  "question": "What are all the characters?",
  "top_k": 20,
  "filters": {
    "folder": "Characters",
    "tags": ["character"]
  }
}
```

**Response**:
```json
{
  "success": true,
  "query_type": "list_all",
  "strategy_used": "metadata_filter",
  "count": 15,
  "results": [
    {
      "id": "characters_captain_novak_md",
      "content": "Full markdown content...",
      "metadata": {
        "file_path": "Characters/Captain Novák.md",
        "filename": "Captain Novák.md",
        "folder": "Characters",
        "tags": ["character", "military"],
        "modified": "2024-10-15T14:20:00",
        "word_count": 842
      },
      "score": 0.95
    }
  ]
}
```

---

#### POST /create-task
Create a new task file in a vault.

**Request**:
```json
{
  "vault_name": "Red-White",
  "vault_path": "C:\\Users\\...\\Red-White.vault",
  "title": "Review Chapter 5",
  "content": "Need to review chapter 5 draft and make revisions",
  "folder": "Tasks",
  "metadata": {
    "priority": "high",
    "due_date": "2024-10-20"
  }
}
```

**Response**:
```json
{
  "success": true,
  "filepath": "Tasks/Review-Chapter-5.md",
  "indexed": true
}
```

---

#### GET /stats
Get statistics about indexed vaults.

**Response**:
```json
{
  "success": true,
  "vaults": {
    "Red-White": {
      "document_count": 127,
      "last_indexed": "2024-10-17T15:30:00",
      "size_mb": 2.4
    },
    "ThistleRidgeHall": {
      "document_count": 98,
      "last_indexed": "2024-10-17T15:35:00",
      "size_mb": 8.1
    }
  }
}
```

---

## Database Schema

### ChromaDB Collections

Each vault gets its own collection:
- Collection name: `vault_name` (e.g., "Red-White", "ThistleRidgeHall")
- Embedding dimensions: 768 (nomic-embed-text)

### Document Schema

```python
{
  "id": "characters_captain_novak_md",  # Unique document ID
  "document": "Full markdown content...",  # Full text for keyword search
  "embedding": [0.123, -0.456, ...],  # 768-dim vector
  "metadata": {
    # File info
    "file_path": "Characters/Captain Novák.md",
    "filename": "Captain Novák.md",
    "folder": "Characters",
    "extension": "md",

    # Dates
    "created": "2024-01-15T10:30:00",
    "modified": "2024-10-15T14:20:00",
    "indexed": "2024-10-17T15:30:00",

    # Content info
    "size_bytes": 5432,
    "word_count": 842,
    "line_count": 45,

    # Obsidian metadata
    "tags": ["character", "military", "protagonist"],
    "yaml_frontmatter": {
      "title": "Captain Václav Novák",
      "type": "character",
      "status": "active",
      "custom_field": "custom_value"
    },

    # Structure
    "headings": ["Overview", "Background", "Personality", "Relationships"],
    "has_wikilinks": true,
    "wikilink_count": 5,
    "linked_files": ["Běla Novák.md", "Red Legion.md"],

    # Search optimization
    "search_text": "captain vaclav novak military character...",  # Preprocessed for search
    "embedding_model": "nomic-embed-text",
    "embedding_version": "1.0"
  }
}
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_query_router.py
def test_list_all_detection():
    router = QueryRouter()
    result = router.classify("What are all the artworks?")
    assert result['type'] == QueryType.LIST_ALL

# tests/test_metadata_extractor.py
def test_yaml_parsing():
    extractor = MetadataExtractor()
    metadata = extractor.extract("test_file.md")
    assert 'yaml_frontmatter' in metadata
    assert metadata['tags'] == ['test', 'example']

# tests/test_hybrid_search.py
def test_search_by_folder():
    results = searcher.search(
        collection,
        "all files",
        {'type': QueryType.FILTER},
        filters={'folder': 'Characters'}
    )
    assert all('Characters' in r['metadata']['folder'] for r in results)
```

### Integration Tests

```python
# tests/test_integration.py
def test_end_to_end_indexing():
    # Index vault
    result = indexer.index_vault("Test-Vault", test_vault_path)
    assert result['count'] > 0

    # Search for documents
    results = searcher.search(collection, "test query")
    assert len(results) > 0

def test_write_and_reindex():
    # Create task
    filepath = writer.create_task("Test Task", "Content")
    assert os.path.exists(filepath)

    # Should be automatically indexed
    time.sleep(2)  # Wait for file watcher
    results = searcher.search(collection, "Test Task")
    assert len(results) > 0
```

### Performance Tests

```python
# tests/test_performance.py
def test_indexing_speed():
    """Should index 1000 files in under 5 minutes"""
    start = time.time()
    indexer.index_vault("Large-Vault", large_vault_path)
    duration = time.time() - start
    assert duration < 300  # 5 minutes

def test_search_speed():
    """Search should return in under 500ms"""
    start = time.time()
    searcher.search(collection, "test query")
    duration = time.time() - start
    assert duration < 0.5  # 500ms
```

---

## Migration Path

### Phase 1: Parallel Deployment (Week 1)

1. Keep existing semantic search working
2. Deploy RAG service alongside
3. Add feature flag to switch between systems
4. Test RAG service with subset of queries

### Phase 2: Gradual Migration (Week 2)

1. Route 25% of traffic to RAG service
2. Monitor error rates and accuracy
3. Increase to 50%, then 75%
4. Compare results with semantic search

### Phase 3: Full Cutover (Week 3)

1. Route 100% to RAG service
2. Deprecate semantic_search.py
3. Remove Smart Connections dependency
4. Clean up old code

### Rollback Plan

Keep semantic search code for 1 month:
- If critical issues found, switch back via feature flag
- Monitor system for 2 weeks before removing old code

---

## Future Enhancements

### Phase 3C: Advanced Features

**Conversation Memory**:
- Store chat history in ChromaDB
- Multi-turn conversations with context
- "Remember" feature across sessions

**Multi-vault Search**:
- Search across all vaults simultaneously
- Cross-reference files between vaults
- Relationship mapping

**Smart Suggestions**:
- "Files related to this one"
- "You might also be interested in..."
- Auto-tagging suggestions

**Advanced Write Operations**:
- Bulk file operations
- Template-based file creation
- Automated backups before writes
- Version control integration

**Analytics Dashboard**:
- Most accessed files
- Search trends
- Vault growth over time
- Tag usage statistics

### Phase 4: Mobile & Sync

- Mobile-optimized interface
- Sync between devices
- Offline mode support
- Progressive Web App (PWA)

---

## Success Criteria

### Functional Requirements

✅ System can index 1000+ files per vault
✅ "List all X" queries return complete results (not just top-K)
✅ Search latency < 500ms for typical queries
✅ File watcher detects changes within 2 seconds
✅ Write operations safely create/update files
✅ Zero data loss during indexing or writes

### Non-Functional Requirements

✅ System uses < 500MB RAM for 3 vaults with 300 files each
✅ ChromaDB database < 100MB on disk
✅ Indexing throughput > 20 files/second
✅ 99.9% uptime for RAG service
✅ All operations logged for debugging

### User Experience

✅ Accurate results for all query types
✅ Fast perceived performance (< 1s to first token)
✅ Clear error messages when things fail
✅ Progress indicators for long operations
✅ Intuitive dashboard for managing vaults

---

## Risk Mitigation

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ChromaDB performance issues | Medium | High | Benchmark early, consider alternatives (Qdrant, Weaviate) |
| Embedding generation slow | High | Medium | Batch processing, caching, consider GPU acceleration |
| File watcher misses changes | Low | High | Add periodic full reindex (daily), checksums |
| Memory leaks | Medium | High | Profiling, automated tests, process monitoring |
| Concurrent write conflicts | Low | High | File locking, transaction logs, backup before write |

### Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| User accidentally deletes vault | Medium | Critical | Automated backups, trash/recycle bin integration |
| Corrupted ChromaDB | Low | High | Regular backups, rebuild from source files |
| Service crashes | Medium | High | Auto-restart (PM2), health checks, monitoring |
| Disk space exhaustion | Low | Medium | Quota warnings, cleanup old embeddings |

---

## Timeline

### Week 1: Core RAG System
- **Day 1**: ChromaDB setup + metadata extraction
- **Day 2**: Hybrid search + file watcher
- **Day 3**: RAG service API + Node.js integration
- **Day 4**: Testing & optimization
- **Day 5**: Write operations + documentation

### Week 2: Testing & Refinement
- Integration testing
- Performance optimization
- Bug fixes
- User acceptance testing

### Week 3: Deployment
- Parallel deployment with feature flags
- Gradual migration
- Monitoring and adjustment
- Documentation finalization

---

## Getting Started (Next Session)

### Preparation Checklist

Before starting implementation:

- [ ] Backup current codebase
- [ ] Review this plan in detail
- [ ] Ensure Python 3.11+ installed
- [ ] Ensure sufficient disk space (2GB+ for ChromaDB)
- [ ] Test vault paths are accessible
- [ ] Confirm Ollama has nomic-embed-text model
- [ ] Create git branch for Phase 3B

### First Commands

```bash
# 1. Install dependencies
cd ollama-service
pip install chromadb==0.4.18 watchdog==3.0.0 python-frontmatter==1.0.1

# 2. Create RAG service directory
cd ..
mkdir rag-service
cd rag-service

# 3. Start with vector_store.py
# (We'll create this together)
```

---

## Questions to Address

Before implementation, confirm:

1. **Vault paths**: Are all vault paths in `C:\Users\redpo\repos\Obsidian\Multi-Vault\`?
2. **File types**: Only `.md` files? Or also `.txt`, `.pdf`, `.canvas`?
3. **Storage location**: Where should ChromaDB store data? Same directory or separate?
4. **Indexing frequency**: Index on startup? Background indexing? Manual trigger?
5. **Write permissions**: Should dashboard be able to modify existing files or only create new ones?
6. **Backup strategy**: Should system auto-backup before writes?

---

## Resources

### Documentation
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Watchdog Documentation](https://python-watchdog.readthedocs.io/)
- [Python Frontmatter](https://python-frontmatter.readthedocs.io/)

### Reference Implementations
- [Obsidian Smart Connections](https://github.com/brianpetro/obsidian-smart-connections)
- [Open WebUI RAG](https://github.com/open-webui/open-webui)
- [LangChain Document Loaders](https://python.langchain.com/docs/integrations/document_loaders/)

### Tools
- [ChromaDB Admin UI](https://github.com/flanker/chromadb-admin)
- [Vector Database Comparison](https://vdbs.superlinked.com/)

---

**Status**: 📋 Ready for Review
**Next Step**: Review plan with user → Begin Day 1 implementation
**Estimated Completion**: 3-5 days (depends on testing depth)

---

*Plan created by: Claude (Anthropic)*
*Date: 2025-10-17*
*Version: 1.0*
