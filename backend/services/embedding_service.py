import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_STORE_DIR = "vector_store"
INDEX_FILE = os.path.join(VECTOR_STORE_DIR, "index.faiss")
METADATA_FILE = os.path.join(VECTOR_STORE_DIR, "metadata.json")


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Load model once (singleton behavior maintained)
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

        # Ensure vector store directory exists
        os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

        self.index = None
        self.metadata = []

        self.load_index()

    def load_index(self):
        if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
            self.index = faiss.read_index(INDEX_FILE)
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            print(f"Loaded existing index with {self.index.ntotal} vectors.")
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
            print("Created new FAISS index.")

    def save_index(self):
        faiss.write_index(self.index, INDEX_FILE)
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def add_chunks(self, chunks: list[str], filename: str):
        if not chunks:
            return

        # 🔥 FIX: Use batching to avoid freezing
        embeddings = self.model.encode(
            chunks,
            batch_size=8,
            show_progress_bar=True
        )

        # 🔥 FIX: Ensure correct dtype for FAISS
        embeddings = np.array(embeddings).astype("float32")

        # Add to FAISS index
        self.index.add(embeddings)

        # Add metadata
        for chunk in chunks:
            self.metadata.append({
                "text": chunk,
                "filename": filename
            })

        self.save_index()

    def search(self, query: str, top_k: int = 3):
        if self.index.ntotal == 0:
            return []

        query_embedding = self.model.encode([query])

        # 🔥 FIX: Ensure dtype consistency
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "score": float(distances[0][i]),
                    "chunk": self.metadata[idx]["text"],
                    "metadata": {
                        "filename": self.metadata[idx]["filename"]
                    }
                })

        return results


# Singleton instance (UNCHANGED)
embedding_service = EmbeddingService()