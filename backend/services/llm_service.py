import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

def generate_answer(query: str, context_chunks: list[dict]) -> str:
    """Generates an answer using local Ollama model given the context."""
    
    # Construct context string
    context_text = "\n\n".join([f"--- Context chunk (Source: {chunk['metadata']['filename']}) ---\n{chunk['chunk']}" for chunk in context_chunks])
    
    prompt = f"""You are a helpful AI assistant. Use the following pieces of retrieved context to answer the user's question. 
If the answer is not in the context, just say that you don't know, don't try to make up an answer.
Always keep your answer concise and accurate.

Context:
{context_text}

Question: {query}

Answer:"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "Error: No response from model.")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to local LLM: {str(e)}. Make sure Ollama is running and 'mistral' model is installed."
