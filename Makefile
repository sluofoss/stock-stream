compile-yf-lambda-cron:
	rm -rf ./datacron/yahoo-finance/pkgs
	rm -f ./datacron/yahoo-finance/deploy_lambda.zip
	echo "start env install"
	pip install --target ./datacron/yahoo-finance/pkgs -q -r ./datacron/yahoo-finance/requirements.txt
	echo "finish env install"
	cd ./datacron/yahoo-finance/pkgs && zip -r -q ../deploy_lambda.zip .
	cd ./datacron/yahoo-finance/ && zip ./deploy_lambda.zip ./source.py 
	cd ./datacron/yahoo-finance/ && zip ./deploy_lambda.zip ./aws_lamdba.py