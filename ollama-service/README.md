# Ollama Python Service

Python Flask service that provides a clean API for interacting with Ollama using the official Python SDK.

## Features

- ✅ Streaming responses (real-time output)
- ✅ Conversation history support
- ✅ Better error handling
- ✅ Embeddings endpoint (for future RAG)
- ✅ Health check endpoint

## Installation

1. Make sure Python 3.8+ is installed:
```bash
python --version
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running:
```bash
ollama serve
```

## Usage

Start the service:
```bash
python app.py
```

The service will be available at `http://localhost:5000`

## API Endpoints

### GET /health
Health check endpoint
```bash
curl http://localhost:5000/health
```

### POST /chat
Chat with Ollama (supports streaming)
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Why is the sky blue?"}
    ],
    "model": "gemma3",
    "stream": true
  }'
```

### GET /models
List available models
```bash
curl http://localhost:5000/models
```

### POST /embed
Generate embeddings (for RAG)
```bash
curl -X POST http://localhost:5000/embed \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma3",
    "input": "Some text to embed"
  }'
```

## Integration with Node.js Server

The Node.js server will call this service instead of using bash scripts. This provides:
- Better reliability
- Streaming support
- Conversation history
- Proper error handling
