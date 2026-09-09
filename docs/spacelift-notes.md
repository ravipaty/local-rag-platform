# Spacelift Setup Notes

## Why Spacelift here
Adds CI/CD to the Terraform layer specifically: instead of running
`terraform apply` manually, pushes to `main` trigger a plan in Spacelift,
gated by an OPA policy check, with manual approval before apply. ArgoCD
still owns the app-layer deployment (the `k8s/` manifests) — Spacelift
only manages the `terraform/` directory (namespace + secret provisioning).

## Free tier fit
- Free plan: 2 users, 1 worker, no time limit, unlimited runs, up to
  200 managed resources. Policy-as-code (OPA) is included free.
- This project provisions a handful of resources (namespace, secret) —
  comfortably within the free tier.

## Prerequisite: push to GitHub
Spacelift needs a VCS integration — it can't run against a local-only
folder. Push this repo to GitHub (or GitLab) first:

```bash
cd ~/local-rag-platform
git init
git add .
git commit -m "Initial commit: local RAG platform on Kubernetes"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/local-rag-platform.git
git push -u origin main
```

## Private worker (required for this setup)
Spacelift's free-tier public worker runs in Spacelift's cloud and cannot
reach a Minikube cluster on your laptop. You need a **private worker** —
a small agent process that runs locally (in WSL2) and polls Spacelift
for jobs instead of Spacelift reaching in to you.

1. In the Spacelift UI: Worker Pools → Create Worker Pool → generates a
   certificate and a docker-compose file for the worker agent.
2. Run the worker in WSL2:
   ```bash
   docker compose -f spacelift-worker-pool.yml up -d
   ```
3. Confirm the worker shows "Connected" in the Spacelift UI.
4. When creating the Stack, select this private worker pool instead of
   the public one.

## Creating the stack
In the Spacelift UI:
- Repository: `local-rag-platform`
- Project root: `terraform`
- Branch: `main`
- Worker pool: your private pool from above
- Attach the policy: `spacelift-policies/no-default-password.rego`
  (Policies → Plan Policies → New → paste the file contents)

## What to demo / talk about in interviews
- GitOps-driven Terraform runs (push → plan → policy check → manual
  approve → apply), separate from the ArgoCD app-deployment path.
- A concrete OPA guardrail (`no-default-password.rego`) blocking an
  insecure default from reaching apply — a real "policy as code"
  example rather than an abstract description.
- Hybrid architecture: cloud-hosted control plane (Spacelift SaaS) with
  a self-hosted private worker reaching into a local-only Kubernetes
  cluster — a fair analogy for how a real org bridges SaaS CI/CD tools
  with on-prem or air-gapped infrastructure.
