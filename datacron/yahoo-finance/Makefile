build-image:
	docker build -f Dockerfile-aws-slim --target final_stage --platform linux/arm64 -t yfinance-cron:aws-slim-r1 .

upload-aws-lambda-image:build-image
	export AWS_ACCOUNT_ID=$$(aws sts get-caller-identity --query Account --output text); \
	export AWS_REGION=$$(aws configure get region); \
	aws ecr get-login-password --region $$AWS_REGION | docker login --username AWS --password-stdin $$AWS_ACCOUNT_ID.dkr.ecr.$$AWS_REGION.amazonaws.com; \
	export ecr_repository_url=$$(cd ../../tf-iaac/yahoo-finance-cron/dev/storage; terraform output ecr_repository_url | tr -d '"'); \
	docker tag yfinance-cron:aws-slim-r1 $$ecr_repository_url:yfinance-cron-aws-slim-latest; \
	time docker push $$ecr_repository_url:yfinance-cron-aws-slim-latest;
	
test-image:build-image
	aws sts get-session-token | jq -r '.Credentials | ["AWS_ACCESS_KEY_ID=" + .AccessKeyId, "AWS_SECRET_ACCESS_KEY=" + .SecretAccessKey, "AWS_SESSION_TOKEN=" + .SessionToken] | .[]' > cred.env
	docker run --platform linux/arm64 -d -v ~/.aws-lambda-rie:/aws-lambda -p 9000:8080 \
    --entrypoint /aws-lambda/aws-lambda-rie \
    --env-file cred.env \
    --env-file local.env \
    yfinance-cron:aws-slim-r1 \
        /usr/local/bin/python -m awslambdaric awslambda.lambda_get_symbols_data_multi; \
	sleep 0.5; \
	curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"time":"2025-01-20T08:12:00Z"}'