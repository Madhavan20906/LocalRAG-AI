LocalRAG‑AI
GitHub stars
GitHub license
Python version

LocalRAG‑AI is a lightweight, self‑contained Retrieval‑Augmented Generation (RAG) framework that runs entirely on your machine.
It combines a local vector store, an LLM (Open‑source or OpenAI API), and an optional PDF/Markdown loader to let you ask natural‑language questions over any document collection without sending data to the cloud.

Table of Contents
Features
Quick Start (Installation & First Run)
Detailed Usage
Configuration
Extending & Contributing
License
Features
Zero‑cloud privacy – everything runs locally; no data leaves your machine.
Pluggable LLM back‑ends – use any Open‑AI‑compatible API, Ollama, LLaMA‑cpp, or HuggingFace models.
Multiple loaders – ingest PDFs, Markdown, plain text, or any custom loader you write.
Hybrid search – combine dense embeddings (FAISS / Chroma) with BM25 for the best of both worlds.
Chat‑style UI – interactive terminal UI that tracks conversation history and citations.
Docker support – one‑command container for reproducible environments.
Extensible CLI – simple argparse based commands that can be wrapped in scripts or notebooks.
Quick Start
Prerequisite – Python ≥ 3.9 and git must be installed.

bash


# 1️⃣ Clone the repo
git clone https://github.com/Madhavan20906/LocalRAG-AI
cd LocalRAG-AI
# 2️⃣ Create a virtual environment (optional but recommended)
python -m venv .venv
.\.venv\Scripts\activate   # on Windows
# source .venv/bin/activate   # on macOS / Linux
# 3️⃣ Install dependencies
pip install -r requirements.txt
# 4️⃣ (Optional) Pull a small open‑source LLM with Ollama
# ollama pull llama2
# Or set your OpenAI API key:
# export OPENAI_API_KEY=sk-...
# 5️⃣ Index a test data folder (replace with your own path)
python rag_cli.py index --source ./sample_docs --store ./vector_store
# 6️⃣ Start chatting
python rag_cli.py chat --store ./vector_store
You should now see an interactive prompt:

>>> How can I help you today?
Feel free to ask questions like “What does the first PDF cover?” and watch the system retrieve relevant passages and generate a concise answer.

Detailed Usage
CLI Overview
Command	Description
rag_cli.py index	Crawl a directory, split documents, embed them, and store vectors.
rag_cli.py chat	Launch an interactive chat over the indexed store.
rag_cli.py eval	Run a simple QA benchmark (useful for testing new models).
rag_cli.py serve	Spin up a lightweight FastAPI server for programmatic access.
Indexing Options
bash


python rag_cli.py index \
  --source /path/to/docs \
  --store ./vector_store \
  --embedder openai:gpt-3.5-turbo-embedding \
  --chunk-size 500 \
  --overlap 50
--embedder can be any provider:model string that localrag.embeddings supports.
--chunk-size/--overlap control how the text is split for optimal retrieval.
Chat Options
bash


python rag_cli.py chat \
  --store ./vector_store \
  --model ollama:llama2 \
  --temperature 0.7 \
  --max-tokens 512
--temperature & --max-tokens work like standard LLM parameters.
Use --no-history to start a stateless session.
Python API (for developers)
python


from localrag import RAGEngine, loaders, embedder
# Load documents
docs = loaders.load_folder("./sample_docs")
# Create an engine (FAISS + BM25 hybrid)
engine = RAGEngine(
    embedder=embedder.OpenAIEmbedding("text-embedding-ada-002"),
    store_path="./vector_store"
)
engine.index(docs)                 # Build the index
answer, citations = engine.ask("What is the main thesis of doc_3?")
print(answer)
print("Sources:", citations)
The API is deliberately simple so you can embed it in notebooks, Streamlit apps, or custom GUIs.

Configuration
All runtime options can also be supplied via a YAML config file (config.yaml). Example:

yaml


embedder:
  provider: openai
  model: text-embedding-ada-002
vector_store:
  type: faiss
  path: ./vector_store
llm:
  provider: ollama
  model: llama2
  temperature: 0.6
  max_tokens: 1024
loader:
  extensions: [".pdf", ".md", ".txt"]
  chunk_size: 400
  overlap: 50
Run with:

bash


python rag_cli.py chat --config config.yaml
Extending & Contributing
Adding a New Document Loader
Create a subclass of localrag.loaders.BaseLoader.
Implement load(path: str) -> List[Document].
Register it in localrag/loaders/__init__.py.
Adding a New Vector Store
Follow the VectorStore abstract class in localrag/store/base.py.
Supported stores out‑of‑the‑box: FAISS, Chroma, Milvus, Weaviate.

Contributing Guide
Fork the repository.
Create a feature branch (git checkout -b feat/your-feature).
Write tests in tests/.
Run pytest locally – all CI jobs must pass.
Submit a Pull Request with a clear description and changelog entry.
Please adhere to the PEP 8 style guide and run black / isort before committing.

License
Distributed under the MIT License. See LICENSE for full text.

✨ Happy RAG‑ing!
If you run into any issues, feel free to open an issue on the repo or drop a comment in the Discussions section. Your feedback helps make LocalRAG‑AI even better.
