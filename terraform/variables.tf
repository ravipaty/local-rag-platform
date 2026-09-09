variable "kubeconfig_path" {
  description = "Path to the kubeconfig file (Minikube default)"
  type        = string
  default     = "~/.kube/config"
}

variable "namespace" {
  description = "Namespace for the RAG platform"
  type        = string
  default     = "rag-platform"
}

variable "postgres_db" {
  type    = string
  default = "ragdb"
}

variable "postgres_user" {
  type    = string
  default = "raguser"
}

variable "postgres_password" {
  type      = string
  sensitive = true
  default   = "changeme" # override via terraform.tfvars, never commit real value
}
