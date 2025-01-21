AWS_ACCCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

AWS_REGION=$(aws configure get region)

echo $AWS_ACCCOUNT_ID 
echo $AWS_REGION

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

#TODO parametrize the dev env
ecr_repository_url=$(cd tf-iaac/yahoo-finance-cron/dev/storage; terraform output ecr_repository_url | tr -d '"')
echo $ecr_repository_url

docker tag yfinance-cron:aws-slim-r1 $ecr_repository_url:yfinance-cron-aws-slim-latest
time docker push $ecr_repository_url:yfinance-cron-aws-slim-latest