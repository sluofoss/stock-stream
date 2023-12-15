compile-yf-lambda-cron:
	rm -rf ./datacron/yahoo-finance/pkgs
	rm -f ./datacron/yahoo-finance/deploy_lambda.zip
	pip install --target ./datacron/yahoo-finance/pkgs -r ./datacron/yahoo-finance/requirements.txt
	zip -r ./datacron/yahoo-finance/deploy_lambda.zip ./datacron/yahoo-finance/pkgs
	zip ./datacron/yahoo-finance/deploy_lambda.zip ./datacron/yahoo-finance/source.py ./datacron/yahoo-finance/aws_lambda.py