provider "aws" {
  region = "us-east-1"
}

resource "aws_eks_cluster" "academy" {
  name     = "liceu-academy"
  role_arn = aws_iam_role.eks.arn

  vpc_config {
    subnet_ids = [
      "subnet-1",
      "subnet-2"
    ]
  }
}
