📄 LocalRAG-AI
Chat with your PDFs using a fully local RAG pipeline — no API keys, no data leaving your machine.

LocalRAG-AI is a full-stack web application that lets you upload PDF documents, index them locally, and ask natural language questions. The system retrieves relevant passages and generates accurate answers with source citations, all running on your own hardware.

https://img.shields.io/github/last-commit/Madhavan20906/LocalRAG-AI
https://img.shields.io/badge/python-3.9+-blue
https://img.shields.io/badge/node-18+-green
https://img.shields.io/badge/ollama-mistral-orange

✨ Features
🔒 100% local – No external APIs, no data sharing, complete privacy.

💬 Chat with your PDFs – Ask questions in natural language.

📎 Source citations – Each answer references the original PDF and page.

🧠 RAG pipeline – Uses sentence-transformers, FAISS, and Ollama.

🎨 Modern UI – Built with React + Vite and a custom premium design system.

⚡ Fast – Asynchronous FastAPI backend, responsive frontend.

🧱 Tech Stack
Layer	Technologies
Backend	FastAPI, sentence-transformers, FAISS, LangChain text splitters, requests
Frontend	React, Vite, Vanilla CSS, lucide-react icons
LLM & Embeddings	Ollama (mistral), local embedding model (all-MiniLM-L6-v2 style)
📋 Prerequisites
Before you begin, make sure you have the following installed:

Python 3.9+

Node.js 18+

Ollama – Download here

Then pull the Mistral model:

bash
ollama run mistral
The first pull might take a few minutes. Once done, Ollama will keep the model ready locally.

🚀 Getting Started
1. Clone the repository
bash
git clone https://github.com/Madhavan20906/LocalRAG-AI.git
cd LocalRAG-AI
2. Backend setup
bash
cd backend
pip install -r requirements.txt
python main.py
The backend API will be available at http://localhost:8000

3. Frontend setup
Open a new terminal and run:

bash
cd frontend
npm install
npm run dev
Visit http://localhost:5173 to use the app.

🖥️ Usage
Upload one or more PDF files using the UI.

Wait for the system to chunk and index the documents (FAISS vector store).

Type your question in the chat box.

Get an answer with citations pointing to the source PDF and text snippet.

📁 Project Structure
text
LocalRAG-AI/
├── backend/               # FastAPI app
│   ├── main.py            # API endpoints & orchestration
│   ├── requirements.txt   # Python dependencies
│   └── ...
├── frontend/              # React + Vite app
│   ├── src/               # UI components & styles
│   ├── package.json
│   └── ...
└── README.md
🧠 How it works (Local RAG pipeline)
Ingestion – PDFs are loaded, split into overlapping chunks.

Embedding – Each chunk is converted into a vector using a local sentence-transformer model.

Storage – Vectors are stored and indexed with FAISS for fast similarity search.

Query – Your question is embedded and compared against stored vectors.

Retrieval – Top-k relevant chunks are retrieved.

Generation – Retrieved chunks + question are sent to local Ollama (mistral) to generate an answer.

Citation – The response includes references to source documents.

🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve functionality, UI, or documentation.

📄 License
This project is open source and available under the MIT License.

🙌 Acknowledgments
Ollama for easy local LLM management

Sentence Transformers

FAISS

FastAPI

React + Vite

Made with ❤️ by Madhavan — keep your documents intelligent and private.
