resource "aws_iam_instance_profile" "instance-profile" {
  name = "Jenkins-instance-profile-2"
  role = aws_iam_role.iam-role.name
}