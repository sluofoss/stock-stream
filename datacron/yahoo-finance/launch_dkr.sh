docker build --platform linux/amd64 -t yfinance-cron:dev .
aws sts get-session-token | jq -r '.Credentials | ["AWS_ACCESS_KEY_ID=" + .AccessKeyId, "AWS_SECRET_ACCESS_KEY=" + .SecretAccessKey, "AWS_SESSION_TOKEN=" + .SessionToken] | .[]' > cred.env
docker run --platform linux/amd64 \
    -d -p 9000:8080 \
    --env ENTRY_POINT=src.domain.sample_command.handler \
    --env-file cred.env \
    --env-file local.env \
    yfinance-cron:dev
    