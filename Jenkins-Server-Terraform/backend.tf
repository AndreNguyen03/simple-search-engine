terraform {
  backend "s3" {
    bucket         = "simple-search-engine-tfstate"
    region         = "ap-southeast-1"
    key            = "Search-Engine/Jenkins-Server-TF/terraform.tfstate"
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