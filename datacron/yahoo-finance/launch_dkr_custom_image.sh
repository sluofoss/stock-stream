docker run --platform linux/amd64 -d -v ~/.aws-lambda-rie:/aws-lambda -p 9000:8080 \
    --entrypoint /aws-lambda/aws-lambda-rie \
    --env-file cred.env \
    --env-file local.env \
    yfinance-cron:aws-slim-r1 \
        /usr/local/bin/python -m awslambdaric awslambda.lambda_get_symbols_data_multi

curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"time":"2024-12-17T08:12:00Z"}'