# Project Context for Claude Code

This file summarizes decisions made in a planning conversation before this
project's code existed, so Claude Code has the same context without needing
it re-explained.

## Who / why
Built by a DevOps/Cloud Architect (20+ years, Director-level, GCP/AWS/Azure,
Kubernetes, Terraform, Zero Trust, MLOps) as a hands-on portfolio project
while job searching, to keep skills sharp and produce a public GitHub repo
that maps directly to resume claims.

## What this project is
A local Retrieval-Augmented Generation (RAG) platform, deployed like real
infrastructure (containerized, orchestrated, provisioned via IaC, shipped
via GitOps) — not just a chatbot demo. Runs on a laptop: Acer Helios 16,
RTX 5070 Ti GPU, 32GB RAM, WSL2 (Ubuntu) on Windows.

## Stack decisions and why (don't relitigate these without reason)
- **Vector DB: Postgres + pgvector**, not Qdrant. Qdrant was originally
  planned but dropped as too heavy to run alongside K8s + Ollama on one
  laptop. pgvector was chosen deliberately over lighter options (ChromaDB,
  SQLite+sqlite-vec) because it's a stronger interview story: shows
  layering vector search into infra teams already trust, rather than
  introducing a new specialized system.
- **Observability: MLflow only** for LLM-call tracing — Langfuse was
  considered and dropped as redundant since MLflow's `@mlflow.trace`
  already covers latency/tokens/prompt versioning.
- **Infra metrics: Metrics Server + Prometheus/Grafana (minimal profile)**.
  Kiali/service mesh explicitly rejected as overkill for a 3-4 service
  laptop project.
- **Distributed tracing: Grafana Tempo** (not Jaeger) — chosen because it
  shares the same Grafana UI already used for Prometheus, avoiding a
  second dashboard to context-switch into.
- **LLM serving: Ollama (local, default)**, with an **optional AWS Bedrock
  provider** behind a shared abstraction (`app/providers/`). Bedrock is
  NOT meant to run continuously — no free tier exists, only $100–200 in
  credits that expire after 6 months. Bedrock's purpose here is narrowly
  to demonstrate a provider-abstraction pattern and IAM least-privilege
  setup, not to be a primary path. See `docs/bedrock-notes.md`.
- **GitOps: ArgoCD** deploys the `k8s/` manifests. **Terraform** only
  provisions what needs to exist before GitOps takes over (namespace,
  initial secret) — Terraform and ArgoCD are intentionally scoped
  separately, not overlapping.
- **CI/CD for the Terraform layer: Spacelift**, chosen for its free tier
  (2 users, 1 worker, unlimited runs, OPA policy-as-code included free).
  Requires a **private worker** running locally (WSL2, via docker-compose)
  because Spacelift's free public worker cannot reach a laptop-local
  Minikube cluster. See `docs/spacelift-notes.md` — this is not yet wired
  up; the repo needs to be pushed to GitHub first.
- **Security**: Network Policies enforce default-deny + explicit allow
  (Zero Trust baseline) — see `k8s/network-policies/zero-trust-defaults.yaml`.
  Secrets must be sealed (`kubeseal`) before ever being committed to git;
  `k8s/postgres/secret.yaml` as it exists now is a plaintext placeholder
  and should never be pushed as-is.

## Current state / where we left off
- Postgres + pgvector confirmed working locally via Docker (`pgvector 0.8.6`
  verified installed in the `ragdb` database).
- Ollama installed on Windows (PowerShell install), reachable from WSL2 via
  forwarded `localhost:11434` — no separate WSL2 Ollama instance needed.
- Models `llama3.1:8b` and `nomic-embed-text` being pulled.
- Python venv created in `app/`, `requirements.txt` installed with no errors.
- **Not yet done**: running `ingest.py`/`query.py` end-to-end to prove the
  RAG loop; pushing the repo to GitHub; wiring up Spacelift; deploying
  anything to Minikube; Terraform apply; ArgoCD setup; Prometheus/Grafana/
  Tempo observability layer.

## Working style preferences from the human
- Prefers lean/laptop-feasible choices over "most complete" — has
  repeatedly trimmed heavier tools (Qdrant, Langfuse, Jaeger, Kiali,
  service mesh) in favor of lighter alternatives that still tell a
  strong resume/interview story.
- Wants each component to map to something concrete and explainable in
  interviews, not just technically present.
- Is hands-on but says his hands-on skills are "a bit greasy" — walk
  through commands explicitly, verify output at each step, don't assume
  prior steps succeeded silently.
