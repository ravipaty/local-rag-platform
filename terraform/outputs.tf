output "namespace" {
  value = kubernetes_namespace.rag_platform.metadata[0].name
}
