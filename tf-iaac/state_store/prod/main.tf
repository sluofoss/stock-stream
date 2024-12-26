terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
    region = "ap-southeast-2" //sydney
}

module "state_store_dev" {
  source = "../modules/state_store"
  bucket_name = "stock-stream-state-prod"
  table_name = "stock-stream-state-prod"
}