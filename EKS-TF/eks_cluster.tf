module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.28"

  subnet_ids         = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  enable_irsa     = true

  eks_managed_node_groups = {
    worker_group = {
      instance_types = [var.node_instance_type]
      desired_size   = var.node_min_size
      min_size       = var.node_min_size
      max_size       = var.node_max_size
    }
  }

  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}
