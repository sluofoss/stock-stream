FROM public.ecr.aws/lambda/python:3.12


ENV AWS_DEFAULT_REGION=ap-southeast-2
ENV AWS_REGION=ap-southeast-2
ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=
ENV AWS_SESSION_TOKEN=
ENV S3_STORE_BUCKET =
ENV S3_STORE_PARENT_KEY =

COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY requirements-dev.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY awslambda.py ${LAMBDA_TASK_ROOT}
COPY ASX_Listed_Companies_17-12-2023_01-39-05_AEDT.csv ${LAMBDA_TASK_ROOT}
COPY logconfig_aws.yaml ${LAMBDA_TASK_ROOT}
COPY logconfig.yaml ${LAMBDA_TASK_ROOT}

CMD [ "awslambda.lambda_get_symbols_data_multi" ]