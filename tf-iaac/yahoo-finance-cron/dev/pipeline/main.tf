terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.82"
    }
  }

  backend "s3" {
    # This backend configuration is filled in automatically at test time by Terratest. If you wish to run this example
    # manually, uncomment and fill in the config below.
    # do terraform init -backend=../../state_store/dev/backend.hcl
    # no this would be error prone, let's just hard code it for now
    
    # dev shared copy paste (differnet by dev staging prod) 
    bucket = "stock-stream-state-dev"
    region = "ap-southeast-2"
    dynamodb_table = "stock-stream-state-dev"
    encrypt = true

    # unique to this folder (differnent by service)
    key = "yahoo-finance-cron/terraform.tfstate"
  }
}
provider "aws" {
    region = "ap-southeast-2" //sydney
}

module "pipeline" {
  source = "../../modules/pipeline/"
  env = "dev"
  code_bucket_name    = data.terraform_remote_state.storage.outputs.s3_bucket_id
  data_bucket_name    = data.terraform_remote_state.storage.outputs.s3_bucket_id
  ecr_repository_url  = data.terraform_remote_state.storage.outputs.ecr_repository_url
  ecr_repository_name  = data.terraform_remote_state.storage.outputs.ecr_repository_name
  sns_failure_email   = var.sns_failure_email
}