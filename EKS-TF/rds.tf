resource "aws_db_subnet_group" "default" {
  name       = "default-subnet-group"
  subnet_ids = [data.aws_subnet.subnet.id, aws_subnet.public-subnet2.id]

  tags = {
    Name = "default-subnet-group"
  }
}

resource "aws_db_instance" "postgres_rds" {
  identifier              = "my-postgres-db"
  allocated_storage       = 20
  engine                  = "postgres"
  engine_version          = "15.3"               # chọn version mới nhất nếu muốn
  instance_class          = "db.t3.micro"
  db_name                 = var.rds_db_name       # ví dụ: "mydatabase"
  username                = var.rds_username
  password                = var.rds_password
  db_subnet_group_name    = aws_db_subnet_group.default.name
  vpc_security_group_ids  = [data.aws_security_group.sg-default.id]
  skip_final_snapshot     = true
  publicly_accessible     = false
  multi_az                = false

  # Thiết lập maintenance window, backup, và các option khác nếu cần
  backup_retention_period = 7
  maintenance_window      = "Mon:00:00-Mon:03:00"
}
