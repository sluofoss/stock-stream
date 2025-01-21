# ecr private repo
resource "aws_ecr_repository" "stock_stream_images" {
  name                 = "stock_stream_images-${var.env_name}"
  image_tag_mutability = "MUTABLE"  # or "IMMUTABLE" based on your requirement
  image_scanning_configuration {
    scan_on_push = true
  }
}
resource "aws_ecr_lifecycle_policy" "stock_stream_policy" {
  repository = aws_ecr_repository.stock_stream_images.name
  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description   = "Keep only 10 images"
        selection     = {
          countType        = "imageCountMoreThan"
          countNumber      = 10
          tagStatus        = "tagged"
          tagPrefixList   = ["dev"]
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}