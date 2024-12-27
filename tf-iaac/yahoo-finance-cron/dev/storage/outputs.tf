output "s3_bucket_arn" {
  value       = module.storage.s3_bucket_arn
  description = "The ARN of the S3 bucket"
}

output "s3_bucket_id" {
  value       = module.storage.s3_bucket_id
  description = "The ID/Name of the S3 bucket"
}