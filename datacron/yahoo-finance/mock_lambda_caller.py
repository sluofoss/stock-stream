import dotenv

from awslambda import lambda_get_symbols_data_multi

dotenv.load_dotenv()

import sys
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
h = logging.FileHandler('./lambda.log')
h.setLevel(logging.DEBUG)
logger.addHandler(h)
logger.info("mock started")

logging.getLogger('yfinance').addHandler(logging.FileHandler('./lambda.log'))
logging.getLogger('awslambda').addHandler(logging.FileHandler('./lambda.log'))
logging.getLogger('source').addHandler(logging.FileHandler('./lambda.log'))

event = {'time':'2023-12-14'}
context = None
lambda_get_symbols_data_multi(event, context)
