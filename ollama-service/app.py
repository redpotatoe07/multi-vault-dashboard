from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import ollama
import json
import os
import sys

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint to verify Ollama connection"""
    try:
        ollama.list()
        return jsonify({
            'status': 'ok',
            'ollama': 'connected',
            'service': 'ollama-python-service'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'ollama': 'disconnected',
            'error': str(e),
            'message': 'Make sure Ollama is running with: ollama serve'
        }), 503

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint that supports both streaming and non-streaming responses.

    Expected JSON body:
    {
        "messages": [{"role": "user", "content": "question"}],
        "model": "gemma3",
        "stream": true
    }
    """
    try:
        data = request.json
        messages = data.get('messages', [])
        model = data.get('model', 'gemma3')
        stream = data.get('stream', True)

        if not messages:
            return jsonify({'error': 'Messages are required'}), 400

        # Streaming response
        if stream:
            def generate():
                try:
                    response = ollama.chat(model=model, messages=messages, stream=True)
                    for chunk in response:
                        # Convert chunk to dict if it's not already
                        if hasattr(chunk, 'model_dump'):
                            chunk_dict = chunk.model_dump()
                        elif hasattr(chunk, 'dict'):
                            chunk_dict = chunk.dict()
                        elif isinstance(chunk, dict):
                            chunk_dict = chunk
                        else:
                            chunk_dict = {'message': {'content': str(chunk)}}

                        # Send each chunk as Server-Sent Event (SSE)
                        yield f"data: {json.dumps(chunk_dict)}\n\n"
                except ollama.ResponseError as e:
                    error_data = {
                        'error': str(e),
                        'status_code': e.status_code if hasattr(e, 'status_code') else 500
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"
                except Exception as e:
                    error_data = {'error': str(e)}
                    yield f"data: {json.dumps(error_data)}\n\n"

            return Response(generate(), mimetype='text/event-stream')

        # Non-streaming response
        else:
            response = ollama.chat(model=model, messages=messages)
            return jsonify(response)

    except ollama.ResponseError as e:
        return jsonify({
            'error': str(e),
            'status_code': e.status_code if hasattr(e, 'status_code') else 500
        }), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/models', methods=['GET'])
def list_models():
    """List all available Ollama models"""
    try:
        models = ollama.list()
        return jsonify({
            'success': True,
            'models': models
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/embed', methods=['POST'])
def embed():
    """
    Generate embeddings for text (for future RAG implementation)

    Expected JSON body:
    {
        "model": "gemma3",
        "input": "text to embed" or ["text1", "text2"]
    }
    """
    try:
        data = request.json
        model = data.get('model', 'gemma3')
        input_text = data.get('input')

        if not input_text:
            return jsonify({'error': 'Input text is required'}), 400

        response = ollama.embed(model=model, input=input_text)
        return jsonify({
            'success': True,
            'embeddings': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/semantic-search', methods=['POST'])
def semantic_search_endpoint():
    """
    Find relevant files using semantic search with Smart Connections embeddings

    Expected JSON body:
    {
        "question": "What are the characters?",
        "vault_path": "C:\\Users\\..\\Red-White.vault",
        "top_k": 15
    }
    """
    try:
        from semantic_search import find_relevant_files

        data = request.json
        question = data.get('question')
        vault_path = data.get('vault_path')
        top_k = data.get('top_k', 15)

        if not question or not vault_path:
            return jsonify({
                'success': False,
                'error': 'Both question and vault_path are required'
            }), 400

        # Find relevant files using semantic search
        results = find_relevant_files(question, vault_path, model='nomic-embed-text', top_k=top_k)

        return jsonify({
            'success': True,
            'results': [{'path': path, 'score': float(score)} for path, score in results]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print('\n' + '='*60)
    print('Ollama Python Service Starting...')
    print('='*60)

    # Check if Ollama is available
    try:
        ollama.list()
        print('[OK] Ollama connection successful')
    except Exception as e:
        print('[WARNING] Cannot connect to Ollama')
        print(f'   Error: {e}')
        print('   Make sure Ollama is running with: ollama serve')

    print('\nService will be available at: http://localhost:5000')
    print('Endpoints:')
    print('   GET  /health           - Health check')
    print('   POST /chat             - Chat with Ollama (streaming)')
    print('   GET  /models           - List available models')
    print('   POST /embed            - Generate embeddings')
    print('   POST /semantic-search  - Find relevant files using Smart Connections')
    print('\n' + '='*60 + '\n')

    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
