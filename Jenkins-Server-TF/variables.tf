variable "aws_region" {
  default = "us-east-1"
}

variable "ami_id" {
  default = "ami-0c94855ba95c71c99" # Amazon Linux 2
}

variable "instance_type" {
  default = "t2.medium"
}

variable "key_name" {
  description = "EC2 Key Pair name"
}

variable "my_ip" {
  description = "Your IP with /32"
}
