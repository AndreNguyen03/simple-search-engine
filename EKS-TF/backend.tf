terraform {
  backend "s3" {
    bucket         = "my-aws-bucket0301"     
    key            = "Search-Engine/EKS-TF/terraform.tfstate"
    region         = "ap-southeast-1"
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
