variable "vpc-name" {}
variable "igw-name" {}
variable "rt-name2" {}
variable "subnet-name" {}
variable "subnet-name2" {}
variable "security-group-name" {}
variable "iam-role-eks" {}
variable "iam-role-node" {}
variable "iam-policy-eks" {}
variable "iam-policy-node" {}
variable "cluster-name" {}
variable "eksnode-group-name" {}
variable "rds_username" {
  default = "admin"
}

variable "rds_password" {
  default = "Admin12345678!"
}

variable "rds_db_name" {
  default = "mydatabase"
}