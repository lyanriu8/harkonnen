from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import sqlite3


class RagStore:
    def __init__(self, base_dir: Path | None = None):
        # allow automatic path detection if user doesn't pass base_dir
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent

        self.base = base_dir
        
        # Load FAISS index
        self.index = faiss.read_index(str(self.base / "ticker_vectors.faiss"))

        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Open SQLite
        self.conn = sqlite3.connect(self.base / "companies.sqlite")
        self.cursor = self.conn.cursor()


    def search(self, text: str, k: int = 5):
        """Return top-k most semantically similar tickers."""
        
        # 1. Embed query
        q_vec = self.model.encode([text], convert_to_numpy=True)
        faiss.normalize_L2(q_vec)

        # 2. FAISS cosine search
        distances, indices = self.index.search(q_vec, k)

        # 3. Map FAISS indices → tickers/descriptions
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            row = self.cursor.execute(
                "SELECT ticker, description FROM companies WHERE id=?",
                (int(idx),)
            ).fetchone()

            if row:
                ticker, desc = row
                results.append({
                    "ticker": ticker,
                    "score": float(dist),     # cosine similarity
                    "description": desc
                })

        return results

if __name__ == "__main__":
    rag = RagStore(Path(__file__).resolve().parent)

    results = rag.search("US exports are deteriorating amid China's tariffs on American Exports", k=5)
    for r in results:
        print(r)
    