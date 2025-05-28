provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "cicd_sg" {
  name        = "cicd_security_group"
  description = "Allow Jenkins and SonarQube"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Jenkins
  }

  ingress {
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # SonarQube
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "cicd_server" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  vpc_security_group_ids      = [aws_security_group.cicd_sg.id]
  user_data                   = file("user_data.sh")
  associate_public_ip_address = true

  tags = {
    Name = "Jenkins-SonarQube-EC2"
  }
}
