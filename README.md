# Multi-Vault Dashboard → Custom Knowledge Management System

**Web-based command center** for managing 9 Obsidian vaults (1,269 markdown files) with **AI-powered RAG search**.

**Current Version**: 0.4.0 (Dashboard phase)
**Long-term Vision**: Evolve into full custom knowledge base + project management web app

> 📖 **See [VISION.md](VISION.md)** for the complete long-term vision and evolution path

---

## 🎯 What This Project Is

**Today (Dashboard):**
- View and search across 9 vaults
- RAG-powered hybrid search (semantic + metadata + keyword)
- Vault statistics and overview
- AI chat integration (Claude, Ollama)

**Tomorrow (Custom App):**
- **+ Edit files** from web browser (markdown editor)
- **+ Git integration** (version control, cloud backup)
- **+ Project management** (timelines, kanban, tasks, deadlines)
- **+ Mobile access** (responsive web app, accessible anywhere)
- **→ Replace Obsidian** as primary interface (while keeping files compatible)

**The Goal:** A custom, web-based knowledge management system tailored exactly to your workflow, with your markdown files backed by Git and accessible anywhere.

## Quick Start

### Prerequisites
1. **Node.js** (v14+ recommended)
2. **Python** (v3.8+ recommended)
3. **Ollama** (for local AI) - [Install from ollama.com](https://ollama.com)

### Installation

```bash
# 1. Install Node.js dependencies
npm install

# 2. Install Python dependencies
cd ollama-service
pip install -r requirements.txt
cd ..

# 3. Make sure Ollama is running
ollama serve

# 4. Pull a model (if not already done)
ollama pull gemma3
```

### Running the Application

You need to run **three services**:

**Terminal 1 - RAG Service (NEW!):**
```bash
cd rag-service
python app.py
# Runs on port 5001
```

**Terminal 2 - Chat Service:**
```bash
cd ollama-service
python app.py
# Runs on port 5000
```

**Terminal 3 - Dashboard:**
```bash
npm start
# Runs on port 3000
```

**Access Points:**
- **Dashboard**: http://localhost:3000
- **RAG API**: http://localhost:5001
- **Chat API**: http://localhost:5000

## Finding Your PC IP Address

**Windows:**
```bash
ipconfig
# Look for "IPv4 Address" under your active network adapter
```

**Example**: If your PC IP is `192.168.1.100`, access from iPhone at `http://192.168.1.100:3000`

## Project Structure

```
multi-vault-dashboard/
├── server.js            # Express server (Node.js) - Port 3000
├── vault-scanner.js     # Vault file system scanner
│
├── rag-service/         # NEW: RAG System (Phase 3B) - Port 5001
│   ├── app.py          # Flask REST API (8 endpoints)
│   ├── vector_store.py # ChromaDB wrapper
│   ├── indexer.py      # Vault indexing (11 docs/sec)
│   ├── hybrid_search.py# Intelligent search
│   ├── query_router.py # Query classification
│   ├── metadata_extractor.py # File parsing
│   ├── file_watcher.py # Auto-indexing
│   └── requirements.txt
│
├── ollama-service/      # Chat service - Port 5000
│   ├── app.py          # Flask API (chat endpoint)
│   └── requirements.txt
│
├── public/              # Frontend
│   ├── index.html      # Main dashboard
│   ├── app.js          # Frontend JS
│   └── style.css       # Styling
│
└── docs/                # Documentation
    ├── PHASE_3B_COMPLETE.md # RAG system summary
    └── README.md        # This file
```

## Configuration

Edit `server.js` to set your vault location:
```javascript
const VAULT_ROOT = 'C:\\Users\\redpo\\repos\\Obsidian\\Multi-Vault';
```

## Features

### Phase 1 & 2 (Complete)
- ✅ View all 8 vaults at a glance
- ✅ File count statistics per vault
- ✅ Recent file changes
- ✅ Cross-vault search
- ✅ Mobile-responsive design
- ✅ Dual AI integration (Ollama + Claude)
- ✅ Chat interface with markdown rendering

### Phase 3A (v0.2.0)
- ✅ **Python SDK integration** - Replace bash scripts with proper ollama-python SDK
- ✅ **Streaming responses** - See AI responses word-by-word in real-time
- ✅ **Better error handling** - More reliable AI interactions
- ✅ **Cleaner architecture** - Microservice pattern (Node.js + Python)

### Phase 3B (v0.3.0) - RAG System
- ✅ **Hybrid Search** - Intelligent query routing (5 query types)
- ✅ **ChromaDB Integration** - Vector database with 1,269 documents indexed
- ✅ **Metadata Filtering** - Solves "list all X" queries (100% accuracy!)
- ✅ **Auto-Indexing** - Real-time file watcher
- ✅ **REST API** - 8 endpoints for search, indexing, management
- ✅ **Production Ready** - 11 docs/sec indexing, <1s search
- ✅ **Database Persistence** - Fixed critical bug, data persists across restarts

### Phase 3C (NEW - v0.4.0) - Unified Search Interface 🎉
- ✅ **Single Search Bar** - One unified "Search & Ask" interface
- ✅ **Three Modes** - RAG Search, Claude Pro, Ollama (Fast)
- ✅ **Smart Routing** - Automatically routes to correct backend based on mode
- ✅ **Debug Toggle** - Visual button for query diagnostics
- ✅ **Clean UI** - Removed duplicate search bars
- ✅ **Consistent UX** - All results displayed as chat messages

## What's New in v0.4.0? (Phase 3C - Unified Interface)

**The Problem We Solved:**
- **Before**: Two confusing search bars (top search + AI chat section)
- **After**: ONE unified "Search & Ask" interface with three modes

**What Changed:**

1. **Unified Interface**
   - Single search bar with dropdown selector
   - Three modes: RAG Search, Claude Pro, Ollama (Fast)
   - All results displayed as chat messages
   - Consistent user experience

2. **RAG Search Integration**
   - Search mode fetches from RAG backend
   - Displays file results with vault icons
   - Shows folder paths and metadata
   - Debug mode shows query type and strategy

3. **Debug Toggle**
   - Visual button (no keyboard conflicts)
   - Green indicator when active
   - Shows query classification details
   - Displays relevance scores

4. **Critical Bug Fix**
   - Fixed ChromaDB persistence issue
   - Database now survives restarts
   - No more re-indexing required!

**See [CHANGELOG.md](CHANGELOG.md) for complete version history**

## Troubleshooting

### Python service won't start
- Make sure Python 3.8+ is installed: `python --version`
- Install dependencies: `cd ollama-service && pip install -r requirements.txt`

### Ollama not connecting
- Start Ollama: `ollama serve`
- Verify it's running: `ollama list`
- Pull a model: `ollama pull gemma3`

### Frontend shows "Ollama Offline"
- Make sure both services are running:
  1. Python service (port 5000)
  2. Node.js server (port 3000)
- Check Python service health: Visit http://localhost:5000/health

### Streaming not working
- Clear browser cache
- Check browser console for errors
- Verify Python service is running

## Documentation

### Current Documentation
- **[README.md](README.md)** - This file - Project overview and quick start
- **[CHANGELOG.md](CHANGELOG.md)** - Complete version history (v0.1.0 to v0.4.0)
- **[NEXT_SESSION.md](NEXT_SESSION.md)** - Quick start guide for next session
- **[SESSION_SUMMARY.md](SESSION_SUMMARY.md)** - Latest session detailed notes

### Reference Documentation
- **[PRD.md](PRD.md)** - Product requirements and roadmap
- **[RESEARCH.md](RESEARCH.md)** - Implementation guide and research
- **[ollama-service/README.md](ollama-service/README.md)** - Python chat service docs

### Archived Documentation
- **[docs/archive/](docs/archive/)** - Historical implementation notes and planning docs
