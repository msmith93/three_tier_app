resource "aws_ecr_repository" "helloworldrepo" {
  name                 = "helloworld"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}