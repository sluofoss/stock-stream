output "s3_bucket_arn" {
  value       = module.storage.s3_bucket_arn
  description = "The ARN of the S3 bucket"
}

output "s3_bucket_id" {
  value       = module.storage.s3_bucket_id
  description = "The ID/Name of the S3 bucket"
}
output "ecr_repository_arn" {
  value       = module.storage.ecr_repository_arn
  description = "The ARN of the ECR Repo"
}

output "ecr_repository_name" {
  value       = module.storage.ecr_repository_name
  description = "The Name of the ECR Repo"
}

output "ecr_repository_registry_id" {
  value       = module.storage.ecr_repository_registry_id
  description = "The registry id of the ECR Repo"
}

output "ecr_repository_url" {
  value       = module.storage.ecr_repository_url
  description = "The URL of the ECR Repo"
}