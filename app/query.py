"""
RAG query: embed the question, retrieve nearest chunks from pgvector,
and generate an answer with the configured LLM provider.

Usage:
    python query.py "What does the document say about X?"
"""

import sys

import mlflow
import psycopg2

import config
from providers import get_provider


def retrieve(conn, query_vector, top_k: int):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT chunk, source, embedding <-> %s::vector AS distance
            FROM documents
            ORDER BY distance ASC
            LIMIT %s;
            """,
            (query_vector, top_k),
        )
        return cur.fetchall()


@mlflow.trace
def answer(question: str) -> str:
    provider = get_provider()
    conn = psycopg2.connect(config.PG_DSN)

    query_vector = provider.embed(question)
    results = retrieve(conn, query_vector, config.TOP_K)
    conn.close()

    context = "\n\n".join(chunk for chunk, _source, _dist in results)
    system = "Answer the question using only the provided context. If the context doesn't contain the answer, say so."
    prompt = f"Context:\n{context}\n\nQuestion: {question}"

    return provider.generate(prompt, system=system)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python query.py "your question"')
        sys.exit(1)

    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(config.MLFLOW_EXPERIMENT)

    question = " ".join(sys.argv[1:])
    print(answer(question))
