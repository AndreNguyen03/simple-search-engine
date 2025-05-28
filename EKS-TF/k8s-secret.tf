resource "kubernetes_secret" "rds_credentials" {
  metadata {
    name      = "rds-credentials"
    namespace = "default"
  }

  data = {
    DB_USERNAME = base64encode(var.rds_username)
    DB_PASSWORD = base64encode(var.rds_password)
    DB_HOST = base64encode(aws_db_instance.postgres_rds.address)
    DB_PORT     = base64encode(tostring(aws_db_instance.postgres_rds.port))
    DB_NAME   = base64encode(var.rds_db_name)
  }

  type = "Opaque"
}
