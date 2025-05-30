provider "aws" {
  region = "ap-southeast-1"  
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"  
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}
