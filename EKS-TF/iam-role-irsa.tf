data "aws_eks_cluster" "cluster" {
  name = var.cluster-name
}

data "aws_eks_cluster_auth" "cluster" {
  name = var.cluster-name
}

resource "aws_iam_openid_connect_provider" "oidc" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["9e99a48a9960b14926bb7f3b02e22da0afd614bb"]
  url             = replace(data.aws_eks_cluster.cluster.identity[0].oidc.issuer, "https://", "")
}

resource "aws_iam_role" "irsa_role" {
  name = "eks-irsa-secrets-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Federated = aws_iam_openid_connect_provider.oidc.arn
      },
      Action = "sts:AssumeRoleWithWebIdentity",
      Condition = {
        StringEquals = {
          "${replace(data.aws_eks_cluster.cluster.identity[0].oidc.issuer, "https://", "")}:sub" = "system:serviceaccount:default:app-service-account"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach_secrets_policy" {
  role       = aws_iam_role.irsa_role.name
  policy_arn = aws_iam_policy.secretsmanager_read_policy.arn
}
