variable "bucket_name" {
  description = "The name of the S3 bucket. Must be globally unique."
  type        = string
  default     = "yahoo-finance-cron"
}

variable "env_name" {
  description = "The env name of the S3 bucket. One of dev, staging, prod"
  type        = string
}
