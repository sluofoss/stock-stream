# TODO: When refactor to env specific, change from variables to locals
variable "code_bucket_name" {
    description = "name of the bucket which all code and packages sit in"
    type        = string
}

variable "data_bucket_name" {
    description = "name of the bucket which all data sit in"
    type        = string
}
