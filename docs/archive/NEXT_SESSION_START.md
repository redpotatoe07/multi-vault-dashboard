# Quick Start Guide - Phase 3B Implementation

**Status**: 📋 Ready to begin
**Estimated Time**: Day 1 (5 hours)
**Goal**: Set up ChromaDB and build metadata extraction

---

## 📚 Documents to Review First

1. **[PHASE_3B_IMPLEMENTATION_PLAN.md](PHASE_3B_IMPLEMENTATION_PLAN.md)** - Complete implementation guide
2. **[SESSION_SUMMARY.md](SESSION_SUMMARY.md)** - What we did last session and why

---

## ✅ Pre-Flight Checklist

Before we start coding:

- [ ] Python 3.11+ installed (`python --version`)
- [ ] Ollama running with nomic-embed-text model (`ollama list`)
- [ ] At least 2GB disk space available
- [ ] Vault paths accessible: `C:\Users\redpo\repos\Obsidian\Multi-Vault\`
- [ ] Current system backed up (optional but recommended)
- [ ] Git working directory clean (optional but recommended)

---

## 🚀 First 10 Minutes

### Step 1: Install Dependencies

```bash
cd c:\Users\redpo\repos\multi-vault-dashboard\ollama-service

# Install ChromaDB and other dependencies
pip install chromadb==0.4.18
pip install watchdog==3.0.0
pip install python-frontmatter==1.0.1
pip install python-markdown==3.5.1
pip install numpy==1.24.3

# Verify installations
python -c "import chromadb; print('ChromaDB:', chromadb.__version__)"
python -c "import watchdog; print('Watchdog:', watchdog.__version__)"
python -c "import frontmatter; print('Frontmatter OK')"
```

### Step 2: Create RAG Service Directory

```bash
cd c:\Users\redpo\repos\multi-vault-dashboard

# Create directory structure
mkdir rag-service
cd rag-service

# Create empty files we'll populate
touch __init__.py
touch vector_store.py
touch metadata_extractor.py
touch indexer.py
touch requirements.txt
```

### Step 3: Create requirements.txt

Create `rag-service/requirements.txt` with:
```txt
chromadb==0.4.18
watchdog==3.0.0
python-frontmatter==1.0.1
python-markdown==3.5.1
numpy==1.24.3
flask==3.0.0
flask-cors==4.0.0
ollama==0.4.8
```

---

## 📝 Day 1 Agenda

### Morning (2-3 hours): ChromaDB Setup

**What we'll build**:
1. `vector_store.py` - ChromaDB wrapper class
2. Test script to verify ChromaDB works

**Key Code** (from implementation plan):
```python
# rag-service/vector_store.py
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
```

**Testing**:
```bash
python test_vector_store.py
# Should see: "✅ ChromaDB initialized successfully"
```

---

### Afternoon (2-3 hours): Metadata Extraction

**What we'll build**:
1. `metadata_extractor.py` - Parse Obsidian files
2. Test with sample vault files

**Key Code** (from implementation plan):
```python
# rag-service/metadata_extractor.py
import frontmatter
import os
from pathlib import Path
from datetime import datetime

class MetadataExtractor:
    def extract(self, file_path, vault_root):
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

        return metadata
```

**Testing**:
```bash
python test_metadata_extractor.py
# Should extract metadata from sample .md file
```

---

## 🎯 Success Criteria for Day 1

By end of Day 1, we should have:

- [x] ChromaDB installed and working
- [x] VaultVectorStore class that can create collections
- [x] MetadataExtractor class that can parse .md files
- [x] Test scripts verifying both components work
- [x] Sample vault file successfully indexed

---

## 📊 Progress Tracking

We'll track progress using todos as we go. Expected todos for Day 1:

1. Install ChromaDB and dependencies
2. Create VaultVectorStore class
3. Test ChromaDB connection
4. Create MetadataExtractor class
5. Test metadata extraction with sample file
6. Create simple indexing test (add 1 document to ChromaDB)

---

## 🔍 What Comes Next (Day 2)

Once Day 1 is complete, Day 2 will focus on:

1. **Indexer** (`indexer.py`) - Index entire vaults
2. **Hybrid Search** (`hybrid_search.py`) - Search logic
3. **Query Router** (`query_router.py`) - Query classification
4. **File Watcher** (`file_watcher.py`) - Auto-indexing

See [PHASE_3B_IMPLEMENTATION_PLAN.md](PHASE_3B_IMPLEMENTATION_PLAN.md) for full Day 2 details.

---

## 💡 Tips for Implementation

1. **Test as you go** - Don't wait until everything is built
2. **Start small** - Get one file indexed before trying to index 100
3. **Use print statements** - Liberal logging helps debug
4. **Check ChromaDB data** - Use ChromaDB's .peek() to verify data
5. **Keep plan open** - Refer to PHASE_3B_IMPLEMENTATION_PLAN.md constantly

---

## 🆘 If You Get Stuck

### Common Issues

**ChromaDB won't install**:
```bash
pip install --upgrade pip
pip install chromadb==0.4.18 --no-cache-dir
```

**Module not found errors**:
```bash
# Make sure you're in the right directory
cd c:\Users\redpo\repos\multi-vault-dashboard\rag-service
python -m pip list  # Check installed packages
```

**File path issues on Windows**:
```python
# Use Path from pathlib
from pathlib import Path
file_path = Path("C:/Users/...").resolve()
```

---

## 📞 Ready to Start?

When you're ready to begin Day 1:

1. Say "Let's start Phase 3B Day 1"
2. I'll guide you through creating each file step-by-step
3. We'll test each component as we build it
4. We'll track progress with todos

---

**Last Updated**: 2025-10-17
**Current Version**: 0.2.1
**Next Version**: 0.3.0 (after Phase 3B complete)

---

**Remember**: We're building this to solve the "list all artworks" problem. The goal is a robust system that handles all query types correctly, not just semantic similarity. Let's build it right! 💪
