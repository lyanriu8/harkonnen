"""
Harkonnen's local RAG database for semantic search 
"""

import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss, numpy as np, sqlite3, yfinance as yf

# BASE_DIR points to: backend/app/nlp/rag
BASE_DIR = Path(__file__).resolve().parent

# RAG_DIR = BASE_DIR (no nested rag folder)
RAG_DIR = BASE_DIR

INDEX_FILE = RAG_DIR / "ticker_vectors.faiss"
META_FILE = RAG_DIR / "companies.sqlite"
TICKER_DF = RAG_DIR / "tickers.csv"

model = SentenceTransformer("all-MiniLM-L6-v2")


def fetch_company_desc(ticker: str) -> str:
    """Fetch long business description using yfinance"""
    t = yf.Ticker(ticker)
    info = t.info
    return info.get("longBusinessSummary", "")


def build():
    """Build the FAISS + SQLite RAG database"""
    RAG_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(TICKER_DF)
    tickers = df["Symbol"].tolist()

    descriptions = []
    for t in tickers:
        try:
            print(f"fetching {t}")
            desc = fetch_company_desc(t)
        except Exception as e:
            print(f"Error fetching description for {t}: {e}")
            desc = ""  # fallback value

        descriptions.append(desc)

    # --- Build FAISS index ---
    vectors = model.encode(descriptions, convert_to_numpy=True)
    faiss.normalize_L2(vectors)

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, str(INDEX_FILE))

    # --- Build SQLite metadata ---
    conn = sqlite3.connect(META_FILE)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY, ticker TEXT, description TEXT)"
    )

    for i, (tic, desc) in enumerate(zip(tickers, descriptions)):
        c.execute("INSERT INTO companies VALUES (?, ?, ?)", (i, tic, desc))

    conn.commit()
    conn.close()

    print("RAG build complete.")


if __name__ == "__main__":
    build()
