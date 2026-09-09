"""
Chunk a text document, embed each chunk, and write it to Postgres/pgvector.

Usage:
    python ingest.py path/to/document.txt
"""

import sys

import mlflow
import psycopg2

import config
from providers import get_provider


def chunk_text(text: str, size: int, overlap: int):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


def ensure_table(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                source TEXT,
                chunk TEXT,
                embedding vector(768)
            );
            """
        )
    conn.commit()


def ingest(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    provider = get_provider()

    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(config.MLFLOW_EXPERIMENT)

    conn = psycopg2.connect(config.PG_DSN)
    ensure_table(conn)

    with mlflow.start_run(run_name=f"ingest:{filepath}"):
        mlflow.log_param("provider", provider.name)
        mlflow.log_param("num_chunks", len(chunks))
        mlflow.log_param("chunk_size", config.CHUNK_SIZE)

        with conn.cursor() as cur:
            for chunk in chunks:
                vector = provider.embed(chunk)
                cur.execute(
                    "INSERT INTO documents (source, chunk, embedding) VALUES (%s, %s, %s)",
                    (filepath, chunk, vector),
                )
        conn.commit()

    conn.close()
    print(f"Ingested {len(chunks)} chunks from {filepath} using {provider.name}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ingest.py <path_to_document>")
        sys.exit(1)
    ingest(sys.argv[1])
