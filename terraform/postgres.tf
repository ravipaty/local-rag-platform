# NOTE: the StatefulSet/Service/init ConfigMap for postgres are deployed
# via k8s/postgres/*.yaml through ArgoCD (GitOps path), not Terraform.
# Terraform here only provisions what needs to exist *before* GitOps
# takes over: the namespace (main.tf) and the initial secret.
#
# In a real environment this secret would come from Vault or Sealed
# Secrets, not a Terraform variable — this is a simplified local stand-in.

resource "kubernetes_secret" "postgres_secret" {
  metadata {
    name      = "postgres-secret"
    namespace = kubernetes_namespace.rag_platform.metadata[0].name
  }

  data = {
    POSTGRES_DB       = var.postgres_db
    POSTGRES_USER      = var.postgres_user
    POSTGRES_PASSWORD  = var.postgres_password
  }

  type = "Opaque"
}
