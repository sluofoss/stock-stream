# TODO: When refactor to env specific, change from variables to locals
variable "code_bucket_name" {
    description = "name of the bucket which all code and packages sit in"
    type        = string
}

variable "data_bucket_name" {
    description = "name of the bucket which all data sit in"
    type        = string
}

variable "timezone" {
    description = "timezone which the event scheduler calls in"
    type        = string
    default     = "Australia/Sydney"
}

variable "env" {
    description = "which environment this is module is deployed in, should be in dev, staging, prod"
    type        = string
}

variable "ecr_repository_url" {
    description = "ecr repo for this environment"
    type        = string
}

variable "ecr_repository_name" {
    description = "ecr repo for this environment"
    type        = string
}


variable "sns_failure_email" {
    description = "email location for sns failure"
    type        = string
}