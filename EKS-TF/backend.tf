terraform {
  backend "s3" {
    bucket         = "my-bucket0301"     
    key            = "Search-Engine/EKS-TF/terraform.tfstate"
    region         = var.aws_region
    dynamodb_table = "Lock-Files"           
    encrypt        = true
  }
  required_version = ">=0.13.0"
  required_providers {
    aws = {
      version = ">= 2.7.0"
      source  = "hashicorp/aws"
    }
  }
}
