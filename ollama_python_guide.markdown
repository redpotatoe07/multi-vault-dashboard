# Installing and Using Ollama with Python

This guide explains how to set up **Ollama**, a tool for running large language models locally, and interact with it using Python. It includes installation steps, basic usage, and example scripts for common tasks like generating text, chatting, and creating embeddings for documents. All steps are designed to work offline on your local machine.

## Prerequisites
- **Operating System**: Windows, macOS, or Linux.
- **Hardware**: A computer with at least 8GB RAM (16GB+ recommended for larger models like Llama3).
- **Python**: Version 3.8 or higher.
- **Disk Space**: Models vary from 4GB (e.g., Llama3 7B) to 50GB+ (e.g., larger models).
- **Internet**: Required for initial downloads; usage is offline afterward.

## Step 1: Install Ollama
1. **Download Ollama**:
   - Visit [ollama.com](https://ollama.com) and download the installer for your OS.
   - **Windows/Linux**: Run the installer or follow terminal instructions.
   - **macOS**: Use Homebrew (`brew install ollama`) or download the binary.
2. **Start Ollama**:
   - Run `ollama serve` in a terminal to start the local server (runs at `http://localhost:11434`).
   - Keep this terminal open while using Ollama.
3. **Pull a Model**:
   - In a new terminal, run `ollama pull llama3` to download the Llama3 model (or choose another, e.g., `mistral`).
   - List available models with `ollama list` or check [Ollama's model library](https://ollama.com/library).

## Step 2: Set Up Python
1. **Install Python**:
   - Ensure Python 3.8+ is installed. Check with `python --version` or `python3 --version`.
   - Download from [python.org](https://www.python.org) if needed.
2. **Install the Ollama Python Library**:
   - Run `pip install ollama` in your terminal to install the official Python client.
   - Verify with `pip show ollama`.

## Step 3: Basic Usage with Python
The `ollama` Python library lets you interact with models via API calls. Below are example scripts for common tasks. Save these as `.py` files and run with `python script_name.py` (ensure `ollama serve` is running).

### Example 1: Simple Text Generation
Generate text from a prompt using a model like Llama3.

```python
import ollama

# Generate text
response = ollama.generate(
    model='llama3',
    prompt='Write a short poem about the moon.'
)

# Print the response
print(response['response'])
```

**Notes**:
- Replace `llama3` with your model name if different.
- The `generate` method is for one-off responses without conversation history.

### Example 2: Chat with Context
Use the `chat` method to maintain a conversation with the model.

```python
import ollama

# Define a conversation
messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': 'What is the capital of France?'},
    {'role': 'assistant', 'content': 'The capital of France is Paris.'},
    {'role': 'user', 'content': 'Tell me more about Paris.'}
]

# Send the chat
response = ollama.chat(model='llama3', messages=messages)

# Print the response
print(response['message']['content'])
```

**Notes**:
- The `messages` list includes roles: `system` (sets model behavior), `user` (your input), and `assistant` (model's prior responses).
- This maintains context for follow-up questions.

### Example 3: Embedding Documents
Create embeddings for text (useful for search or similarity tasks).

```python
import ollama

# Text to embed
text = "The quick brown fox jumps over the lazy dog."

# Generate embedding
embedding = ollama.embeddings(model='nomic-embed-text', prompt=text)

# Print the embedding (a vector of numbers)
print(f"Embedding length: {len(embedding['embedding'])}")
print(embedding['embedding'][:5], "...")  # Show first 5 values
```

**Notes**:
- Use an embedding model like `nomic-embed-text` (pull with `ollama pull nomic-embed-text`).
- Embeddings are vectors for tasks like document similarity or Retrieval-Augmented Generation (RAG).

### Example 4: Reading and Summarizing a File
Read a local text file (e.g., a Markdown note) and summarize it.

```python
import ollama
from pathlib import Path

# Path to your file (replace with your file path)
file_path = Path.home() / "Documents" / "note.md"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Summarize with Ollama
response = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'system', 'content': 'Summarize the following text concisely.'},
        {'role': 'user', 'content': content}
    ]
)

# Print summary
print(response['message']['content'])

# Optionally, save to a new file
output_path = file_path.parent / "summary.md"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f"# Summary\n{response['message']['content']}")
print(f"Summary saved to {output_path}")
```

**Notes**:
- Ensure the file exists and is readable.
- For large files, truncate or chunk content to fit the model's context window (e.g., 8k tokens for Llama3). Use `ollama run llama3 /set parameter num_ctx 32768` to increase context if needed.

## Step 4: Advanced Usage Tips
- **Multiple Models**: Run different models by changing the `model` parameter (e.g., `mistral`, `llama3.1`).
- **Context Window**: Adjust with `ollama run <model> /set parameter num_ctx <size>` (e.g., 32768 for larger inputs).
- **RAG with LangChain**: For document-heavy tasks, use `pip install langchain langchain-community` and integrate with `OllamaEmbeddings` for efficient document indexing.
  ```python
  from langchain_community.embeddings import OllamaEmbeddings
  embeddings = OllamaEmbeddings(model="nomic-embed-text")
  # Use with LangChain's vector stores
  ```
- **Error Handling**: Check if Ollama is running (`ollama ps`) and verify the model is pulled (`ollama list`).
- **Performance**: Use smaller models (e.g., `phi3`) on low-end hardware; larger models (e.g., `llama3:70b`) need 32GB+ RAM or a GPU.

## Troubleshooting
- **Ollama not running**: Ensure `ollama serve` is active. Restart if needed.
- **Model not found**: Run `ollama pull <model>` to download.
- **Connection errors**: Verify Ollama is at `http://localhost:11434`. For CORS issues, set `OLLAMA_ORIGINS=*` (e.g., in PowerShell: `$env:OLLAMA_ORIGINS="*"; ollama serve`).
- **Large files**: Chunk text or use embeddings for RAG to avoid context limits.
- **Python errors**: Ensure `ollama` library is installed (`pip install ollama`) and Python is 3.8+.

## Resources
- [Ollama Documentation](https://ollama.com/docs)
- [Ollama Python Library](https://github.com/ollama/ollama-python)
- [LangChain for Ollama](https://python.langchain.com/docs/integrations/llms/ollama)

This guide should get you started with Ollama and Python for tasks like text generation, chatting, and processing local files. For more advanced integrations (e.g., Obsidian vaults), extend the file-reading script with LangChain or explore Obsidian plugins like Copilot.