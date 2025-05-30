output "cluster_name" {
  description = "EKS Cluster name"
  value       = module.eks.cluster_id
}

output "kubeconfig" {
  description = "Kubeconfig for cluster"
  value       = module.eks.kubeconfig
  sensitive   = true
}

output "load_balancer_controller_sa" {
  value = module.alb_irsa.service_account_name
}
