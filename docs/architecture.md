# Architecture — Local RAG Platform on Kubernetes

## Overview
A locally-run Retrieval-Augmented Generation platform, deployed to Kubernetes
(Minikube) using GitOps, with a swappable LLM backend (local Ollama by default,
optional AWS Bedrock).

## Components
| Layer | Tool |
|---|---|
| LLM serving | Ollama (local), AWS Bedrock (optional) |
| Vector store | Postgres + pgvector |
| Experiment/trace tracking | MLflow |
| Orchestration | Kubernetes (Minikube) |
| Provisioning | Terraform |
| Deployment | ArgoCD (GitOps) |
| Metrics | Metrics Server, Prometheus + Grafana |
| Distributed tracing | OpenTelemetry SDK → Tempo → Grafana |
| Security | Network Policies (Zero Trust), Sealed Secrets, RBAC |

## Data flow
1. `ingest.py` chunks a source document, embeds each chunk via the active
   provider, and writes `(chunk, embedding)` rows to Postgres/pgvector.
2. `query.py` embeds the incoming question, retrieves the nearest chunks via
   pgvector's `<->` distance operator, and passes them as context to the LLM.
3. Every query is wrapped in `@mlflow.trace`, logging latency, token usage,
   and the provider used.

## Diagram
(Add a diagram here — e.g. draw.io export or an ASCII block — once the stack
is running end-to-end.)

## Design decisions worth calling out in interviews
- Chose pgvector over a dedicated vector DB (Qdrant) to avoid a second
  specialized system on a resource-constrained dev machine, and to
  demonstrate integrating vector search into infra teams already trust.
- Chose MLflow tracing over MLflow + Langfuse to avoid redundant
  observability tooling — one tool covers experiment tracking and LLM
  call tracing.
- Backed MLflow tracking server with the existing Postgres instance
  (dedicated `mlflow` DB on the same instance as `ragdb`) rather than SQLite,
  making the tracking server stateless and mirroring production patterns
  (where MLflow runs stateless in K8s backed by managed RDS).
- Provider abstraction (`app/providers/`) decouples the RAG pipeline from
  any single LLM backend — same interface for local (Ollama) and cloud
  (Bedrock), selected via `LLM_PROVIDER` env var.
