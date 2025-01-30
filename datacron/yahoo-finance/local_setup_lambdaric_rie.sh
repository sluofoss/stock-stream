#amd64
mkdir -p ~/.aws-lambda-rie && \
    curl -Lo ~/.aws-lambda-rie/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie && \
    chmod +x ~/.aws-lambda-rie/aws-lambda-rie
#arm64
mkdir -p ~/.aws-lambda-rie-arm64 && \
    curl -Lo ~/.aws-lambda-rie-arm64/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie-arm64 && \
    chmod +x ~/.aws-lambda-rie-arm64/aws-lambda-rie
