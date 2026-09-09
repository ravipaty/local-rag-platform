terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

provider "kubernetes" {
  config_path = var.kubeconfig_path
}

resource "kubernetes_namespace" "rag_platform" {
  metadata {
    name = var.namespace
    labels = {
      "app.kubernetes.io/part-of" = "local-rag-platform"
      "istio-injection"           = "enabled"
    }
  }
}
