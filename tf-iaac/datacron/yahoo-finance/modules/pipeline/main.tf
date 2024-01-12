# example from tf doc
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function

# https://registry.terraform.io/providers/hashicorp/aws/latest/docs
# according to this link, we dont have to define var AWS credential related ENV VAR

# TODO: move `provider` to `dev` and `prod` instead of `modules`
provider "aws" {
    
}

resource "null_resource" "lambda_cron_code_zip" {
    triggers = {
      requirements = filesha1("${local.datacron_yfinance_folder}/awslambda.py")
    }
    provisioner "local-exec" {
      command = <<EOT

        pip3 install -r ${local.requirements_path} -t python/
        zip -r ${local.layer_zip_path} python/
      EOT
  }
}

resource "null_resource" "lambda_cron_layer_zip" {
    triggers = {
      requirements = filesha1("${local.datacron_yfinance_folder}/requirements.py")
    }
    provisioner "local-exec" {
      command = <<EOT
        # set -e
        # apt-get update
        # apt install python3 python3-pip zip -y
        # rm -rf python
        # mkdir python
        pip3 install -r ${local.requirements_path} -t python/
        zip -r ${local.layer_zip_path} python/
      EOT
  }
}

resource "aws_s3_object" "lambda_cron_code_zip" {
  bucket = "${var.code_bucket_name}"
  key    = "/yahoo-finance/lambda_cron_code_zip"
  source = "${local.datacron_yfinance_folder}/awslambda.py"

  # The filemd5() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the md5() function and the file() function:
  # etag = "${md5(file("path/to/file"))}"
  etag = filemd5("${local.datacron_yfinance_folder}/awslambda.py")
}