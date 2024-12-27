output "s3_bucket_arn" {
  value       = aws_s3_bucket.project_storage.arn
  description = "The ARN of the S3 bucket"
}

output "s3_bucket_id" {
  value       = aws_s3_bucket.project_storage.id
  description = "The ID/Name of the S3 bucket"
}