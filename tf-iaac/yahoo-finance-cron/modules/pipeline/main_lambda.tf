# example from tf doc
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function

# https://registry.terraform.io/providers/hashicorp/aws/latest/docs
# according to this link, we dont have to define var AWS credential related ENV VAR


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
  name               = "lambda_yfinance_daily_batch_${var.env}"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role.json
}

# where this is templated from:
# https://stackoverflow.com/questions/57145353/how-to-grant-lambda-permission-to-upload-file-to-s3-bucket-in-terraform
# TODO: Change this to resource base policy instead and/or tighten action permission 
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_policy
resource "aws_iam_policy" "lambda_yfinance_daily_batch_s3_upload" {
  name        = "lambda_yfinance_daily_batch_s3_upload_${var.env}"
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
              "s3:*Object"
          ]
          Resource = "arn:aws:s3:::${var.data_bucket_name}/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_yfinance_daily_batch_s3_upload" {
  role       = aws_iam_role.lambda_yfinance_daily_batch.name
  policy_arn = aws_iam_policy.lambda_yfinance_daily_batch_s3_upload.arn
}

resource "aws_lambda_function" "lambda_yfinance_daily_batch" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.

  image_uri     = "${var.ecr_repository_url}:yfinance-cron-aws-slim-latest"
  function_name = "lambda_yfinance_daily_batch_${var.env}" # TODO: Change this to be environment specific
  role          = aws_iam_role.lambda_yfinance_daily_batch.arn
  #handler       = "awslambda.lambda_get_symbols_data_multi"

  #runtime = "python3.12"

  memory_size = 1024
  package_type = "Image"

  timeout = 900 # 60*15 seconds, or 15 minutes

  environment {
    variables = {
      foo = "bar"
      WORKER_NUM = 5
      #PRINT_DATA_IN_LOG = true
      S3_STORE_BUCKET = var.data_bucket_name
      S3_STORE_PARENT_KEY = "yfinance/min" # TODO: figure out whether this should be hardcoded
      env = var.env
    }
  }
}



#############################
##
##  SCHEDULING (METHOD 1)
##
#############################

# https://docs.aws.amazon.com/scheduler/latest/UserGuide/setting-up.html#setting-up-execution-role
resource "aws_iam_policy" "lambda_yfinance_daily_batch_caller" {
  name        = "lambda_yfinance_daily_batch_caller_${var.env}"
  description = "allow lambda to upload to specific bucket"
  policy      = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action  = "lambda:InvokeFunction"
        Effect  = "Allow"
        Resource = [aws_lambda_function.lambda_yfinance_daily_batch.arn]
      
      }
    ]
  })
}


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
  name                  = "lambda_yfinance_daily_batch_caller_${var.env}"
  assume_role_policy    = data.aws_iam_policy_document.assume_scheduler_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_yfinance_daily_batch_caller" {
  role       = aws_iam_role.lambda_yfinance_daily_batch_caller.name
  policy_arn = aws_iam_policy.lambda_yfinance_daily_batch_caller.arn
}

resource "aws_scheduler_schedule" "lambda_yfinance_daily_batch" {
  name = "lambda_yfinance_daily_batch_${var.env}"
  flexible_time_window {
    mode = "OFF"
  }
  schedule_expression = "cron(0 18 * * ? *)"
  schedule_expression_timezone = var.timezone
  target {
    arn       = aws_lambda_function.lambda_yfinance_daily_batch.arn
    role_arn  = aws_iam_role.lambda_yfinance_daily_batch_caller.arn
  }
}


#############################
##
##  SCHEDULING (METHOD 2 )
##
#############################

##  https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission

/*
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
*/