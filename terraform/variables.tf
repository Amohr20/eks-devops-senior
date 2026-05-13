variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "cluster_name" {
  type    = string
  default = "eks-devops-senior"
}

variable "github_repo" {
  type        = string
  description = "Formato: usuario/repositorio"
}