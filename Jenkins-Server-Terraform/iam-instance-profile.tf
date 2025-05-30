resource "aws_iam_instance_profile" "instance-profile" {
  name = "Jenkins-instance-profile-1"
  role = aws_iam_role.iam-role.name
}