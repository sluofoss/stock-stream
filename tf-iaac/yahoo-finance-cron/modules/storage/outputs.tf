output "s3_bucket_arn" {
  value       = aws_s3_bucket.project_storage.arn
  description = "The ARN of the S3 bucket"
}

output "s3_bucket_id" {
  value       = aws_s3_bucket.project_storage.id
  description = "The ID/Name of the S3 bucket"
}

output "ecr_repository_arn" {
  value       = aws_ecr_repository.stock_stream_images.arn
  description = "The ARN of the ECR Repo"
}

output "ecr_repository_name" {
  value       = aws_ecr_repository.stock_stream_images.name
  description = "The Name of the ECR Repo"
}

output "ecr_repository_registry_id" {
  value       = aws_ecr_repository.stock_stream_images.registry_id
  description = "The registry id of the ECR Repo"
}

output "ecr_repository_url" {
  value       = aws_ecr_repository.stock_stream_images.repository_url
  description = "The URL of the ECR Repo"
}