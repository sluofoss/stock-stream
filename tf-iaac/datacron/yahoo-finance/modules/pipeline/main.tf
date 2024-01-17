# example from tf doc
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function

# https://registry.terraform.io/providers/hashicorp/aws/latest/docs
# according to this link, we dont have to define var AWS credential related ENV VAR

# TODO: move `provider` to `dev` and `prod` instead of `modules`
provider "aws" {
    
}



#############################
##
##  CODE COMPILE & UPLOAD
##
#############################

# Forum suggest moving artifact generation outside of terraform
# https://discuss.hashicorp.com/t/updating-aws-s3-object-resource-without-deleting-previous-files/36698
resource "null_resource" "lambda_yfinance_daily_batch_code_zip" {
    triggers = {
      requirement1 = filesha1("${local.datacron_yfinance_folder}/awslambda.py")
      requirement2 = filesha1("${local.datacron_yfinance_folder}/ASX_Listed_Companies_17-12-2023_01-39-05_AEDT.csv")
    }
    provisioner "local-exec" {
      command = <<EOT
        echo "start zipping lambda code"
        rm -f ${local.datacron_yfinance_folder}/lambda_cron_code.zip
        cd ${local.datacron_yfinance_folder} 
        zip ./lambda_cron_code.zip ./awslambda.py 
        zip ./lambda_cron_code.zip ./ASX_Listed_Companies_17-12-2023_01-39-05_AEDT.csv
        echo "finish zipping lambda code"
      EOT
  }
}

# can be partially replaced with `data "archive_file"`
resource "null_resource" "lambda_yfinance_daily_batch_layer_zip" {
    triggers = {
      requirements = filesha1("${local.datacron_yfinance_folder}/requirements.txt")
    }
    provisioner "local-exec" {
      # https://aws.plainenglish.io/streamlining-serverless-applications-managing-aws-lambda-dependencies-with-layers-and-terraform-18968cf27811
      
      # TODO: remove duplicate packages: boto, pip, etc
      # https://stackoverflow.com/questions/69355100/reducing-python-zip-size-to-use-with-aws-lambda

      command = <<EOT
        # set -e
        # apt-get update
        # apt install python3 python3-pip zip -y
        # rm -rf python
        # mkdir python
        echo "start zipping lambda layer"
        
        rm -rf ${local.datacron_yfinance_folder}/lambda_cron_layer/
        
        rm -f ${local.datacron_yfinance_folder}/lambda_cron_layer.zip

        pip install --target ${local.datacron_yfinance_folder}/lambda_cron_layer/ -q -r ${local.datacron_yfinance_folder}/requirements.txt

	      cd ${local.datacron_yfinance_folder}/lambda_cron_layer/ && zip -r -q ../lambda_cron_layer.zip .

        echo "finish env zipping"
      EOT
  }
}

resource "aws_s3_object" "lambda_yfinance_daily_batch_code_zip" {
  bucket = "${var.code_bucket_name}"
  key    = "yahoo-finance/lambda_cron_code.zip"
  source = "${local.datacron_yfinance_folder}/lambda_cron_code.zip"

  # The filemd5() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the md5() function and the file() function:
  # etag = "${md5(file("path/to/file"))}"
  etag = filemd5("${local.datacron_yfinance_folder}/awslambda.py")

  depends_on = [null_resource.lambda_yfinance_daily_batch_code_zip]
}

resource "aws_s3_object" "lambda_yfinance_daily_batch_layer_zip" {
  bucket = "${var.code_bucket_name}"
  key    = "yahoo-finance/lambda_cron_layer.zip"
  source = "${local.datacron_yfinance_folder}/lambda_cron_layer.zip"

  # The filemd5() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the md5() function and the file() function:
  # etag = "${md5(file("path/to/file"))}"
  etag = filemd5("${local.datacron_yfinance_folder}/requirements.txt") # TODO: this seems to generate cause refresh to happen when there are no change?
  depends_on = [ null_resource.lambda_yfinance_daily_batch_layer_zip ]
}


#############################
##
##  LAMBDA DEFINITION
##
#############################

data "aws_iam_policy_document" "assume_lambda_role" { # TODO: refactor out to main infra module
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_yfinance_daily_batch" {
  name               = "lambda_yfinance_daily_batch_${local.env}"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role.json
}

# where this is templated from:
# https://stackoverflow.com/questions/57145353/how-to-grant-lambda-permission-to-upload-file-to-s3-bucket-in-terraform
# TODO: Change this to resource base policy instead and/or tighten action permission 
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_policy
resource "aws_iam_policy" "lambda_yfinance_daily_batch_s3_upload" {
  name        = "lambda_yfinance_daily_batch_s3_upload_${local.env}"
  description = "allow lambda to upload to specific bucket"
  policy      = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
          Effect = "Allow"
          Action =  [
              "logs:*"
          ]
          "Resource": "arn:aws:logs:*:*:*"
      },
      {
          Effect =  "Allow",
          Action = [
              "s3:*"
          ]
          Resource = "arn:aws:s3:::${var.data_bucket_name}"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_yfinance_daily_batch_s3_upload" {
  role       = aws_iam_role.lambda_yfinance_daily_batch.name
  policy_arn = aws_iam_policy.lambda_yfinance_daily_batch_s3_upload.arn
}

resource "aws_lambda_layer_version" "lambda_yfinance_daily_batch" {
  layer_name    = "lambda_yfinance_daily_batch_${local.env}"
  s3_bucket     = aws_s3_object.lambda_yfinance_daily_batch_layer_zip.bucket
  s3_key        = aws_s3_object.lambda_yfinance_daily_batch_layer_zip.key
  source_code_hash = aws_s3_object.lambda_yfinance_daily_batch_layer_zip.checksum_sha256
}

resource "aws_lambda_function" "lambda_yfinance_daily_batch" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  s3_bucket     = aws_s3_object.lambda_yfinance_daily_batch_code_zip.bucket
  s3_key        = aws_s3_object.lambda_yfinance_daily_batch_code_zip.key
  function_name = "lambda_yfinance_daily_batch_${local.env}" # TODO: Change this to be environment specific
  role          = aws_iam_role.lambda_yfinance_daily_batch.arn
  handler       = "awslambda.lambda_get_symbols_data_multi"

  source_code_hash = aws_s3_object.lambda_yfinance_daily_batch_code_zip.checksum_sha256

  layers        = [aws_lambda_layer_version.lambda_yfinance_daily_batch.arn]

  runtime = "python3.11"

  environment {
    variables = {
      foo = "bar"
      S3_STORE_BUCKET = var.data_bucket_name
      S3_STORE_PARENT_KEY = "yfinance/min" # TODO: figure out whether this should be hardcoded
    }
  }
}



#############################
##
##  SCHEDULING (METHOD 1)
##
#############################

/*
resource "aws_iam_policy" "lambda_yfinance_daily_batch_caller" {
  name        = "lambda_yfinance_daily_batch_caller_${local.env}"
  description = "allow lambda to upload to specific bucket"
  policy      = jsonencode({
    Version   = "2012-10-17",
    statement = {
      sid       = "LambdaAccess"
      effect    = "Allow"
      actions   = ["lambda:InvokeFunction"]
      resources = [aws_lambda_function.lambda_yfinance_daily_batch.arn]
    }
  })
}
*/
#############################
##
##  SCHEDULING (METHOD 2 )
##
#############################

##  https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission

data "aws_iam_policy_document" "assume_scheduler_role" { # TODO: refactor out to main infra module
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}
resource "aws_iam_role" "lambda_yfinance_daily_batch_caller" {
  name                  = "lambda_yfinance_daily_batch_caller_${local.env}"
  assume_role_policy    = data.aws_iam_policy_document.assume_scheduler_role.json
}

resource "aws_scheduler_schedule" "lambda_yfinance_daily_batch" {
  name = "lambda_yfinance_daily_batch_${local.env}"
  flexible_time_window {
    mode = "OFF"
  }
  schedule_expression = "cron(0 18 * * ? *)"
  schedule_expression_timezone = var.timezone
  target {
    arn       = aws_lambda_function.lambda_yfinance_daily_batch.arn
    role_arn  = lambda_yfinance_daily_batch_caller
  }
}

resource "aws_lambda_permission" "lambda_yfinance_daily_batch_scheduler" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_yfinance_daily_batch.function_name
  principal     = "scheduler.amazonaws.com"
  source_arn    = aws_scheduler_schedule.lambda_yfinance_daily_batch.arn
  lifecycle {
    replace_triggered_by = [
      aws_lambda_function.lambda_yfinance_daily_batch
    ]
  }
}