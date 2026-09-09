import os

# LLM backend: "ollama" (default, local) or "bedrock" (cloud, optional)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

# Postgres / pgvector connection
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB = os.getenv("PG_DB", "ragdb")
PG_USER = os.getenv("PG_USER", "raguser")
PG_PASSWORD = os.getenv("PG_PASSWORD", "changeme")

PG_DSN = f"host={PG_HOST} port={PG_PORT} dbname={PG_DB} user={PG_USER} password={PG_PASSWORD}"

# RAG tuning
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K = int(os.getenv("TOP_K", "4"))

# MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_EXPERIMENT = os.getenv("MLFLOW_EXPERIMENT", "local-rag-platform")
