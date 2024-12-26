data "terraform_remote_state" "storage" {
    backend = "s3"
    config = {
        bucket = "stock-stream-state-dev"
        key = "yahoo-finance-cron/storage/terraform.tfstate"
        region = "ap-southeast-2"
    }
}