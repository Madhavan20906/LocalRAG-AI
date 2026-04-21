# Local RAG Web App

A fully local Retrieval-Augmented Generation (RAG) web application with a sleek, premium React frontend and a FastAPI backend. 
It uses `sentence-transformers`, `FAISS`, and a local Ollama instance to index PDFs and answer questions with source citations.

## Prerequisites

1.  **Python 3.9+**
2.  **Node.js 18+**
3.  **Ollama**: Install from [ollama.com](https://ollama.com/) and run the mistral model:
    ```bash
    ollama run mistral
    ```

## Setup & Running

### 1. Backend

Open a terminal and navigate to the backend directory:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the FastAPI server:
```bash
python main.py
```
*The API will be available at http://localhost:8000*

### 2. Frontend

Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```
*Open http://localhost:5173 to view the application.*

## Architecture
- **Backend**: FastAPI, `langchain-text-splitters` for chunking, `sentence-transformers` for embeddings, `faiss-cpu` for vector storage, and `requests` to talk to local Ollama.
- **Frontend**: Vite + React, Vanilla CSS with custom design system, lucide-react for icons.
"# LocalRAG-AI" 
"# LocalRAG-AI" 
