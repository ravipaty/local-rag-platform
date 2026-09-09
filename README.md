# Local RAG Platform on Kubernetes

A self-contained DevSecOps/MLOps practice project: a Retrieval-Augmented
Generation pipeline running entirely on your own laptop, deployed like
production infrastructure — containerized, orchestrated, provisioned with
Terraform, and shipped via GitOps.

## Stack
- **LLM serving:** Ollama (local, default) — optional AWS Bedrock swap-in
- **Vector store:** Postgres + pgvector
- **Tracking/tracing:** MLflow
- **Orchestration:** Kubernetes (Minikube)
- **Provisioning:** Terraform
- **Deployment:** ArgoCD (GitOps)
- **Metrics:** Metrics Server, Prometheus + Grafana (minimal profile)
- **Distributed tracing:** OpenTelemetry SDK → Tempo → Grafana
- **Security:** Network Policies (Zero Trust), Sealed Secrets, RBAC
- **CI/CD for infra:** Spacelift (Terraform plan/apply, policy-as-code via OPA)

## Build order
1. **Validate RAG works standalone** — run Postgres+pgvector via Docker,
   `pip install -r app/requirements.txt`, pull an Ollama model
   (`ollama pull llama3.1:8b`, `ollama pull nomic-embed-text`), then:
   ```
   python app/ingest.py path/to/some/document.txt
   python app/query.py "a question about that document"
   ```
2. **Containerize + deploy to Minikube** using the manifests in `k8s/`.
3. **Add Terraform** (`terraform/`) to provision the namespace and initial
   secret declaratively.
4. **Add ArgoCD** (`argocd/app-of-apps.yaml`) so changes deploy via git push.
5. **Add observability**: MLflow is already wired into `ingest.py`/`query.py`;
   layer in Prometheus/Grafana and Tempo for infra metrics and service-level
   tracing (see `docs/architecture.md`).
6. **Optional: test the Bedrock provider** — see `docs/bedrock-notes.md`
   before running any calls (no free tier, credits expire in 6 months).
7. **Optional: wire up Spacelift for Terraform CI/CD** — see
   `docs/spacelift-notes.md`. Requires pushing this repo to GitHub first,
   and a private worker (in WSL2) since the free tier's public worker
   can't reach a local Minikube cluster.

## Folder structure
```
local-rag-platform/
├── terraform/          # namespace + secret provisioning
├── k8s/                 # postgres, ollama, mlflow manifests + network policies
├── argocd/               # GitOps entrypoint
├── app/
│   ├── providers/        # LLM provider abstraction (ollama, bedrock)
│   ├── ingest.py
│   ├── query.py
│   └── config.py
├── spacelift.yaml         # Spacelift stack config (terraform CI/CD)
├── spacelift-policies/     # OPA/Rego policies for Spacelift plan checks
└── docs/                 # architecture notes, Bedrock cost notes, Spacelift setup
```

## Security notes
- `k8s/postgres/secret.yaml` is a **plaintext placeholder** — seal it with
  `kubeseal` before committing anything to git.
- Network policies default-deny all traffic in the namespace; only explicit
  app → postgres / app → ollama / app → mlflow paths are allowed.
