import dotenv

from awslambda import lambda_get_symbols_data_multi

dotenv.load_dotenv()

event = None
context = None
lambda_get_symbols_data_multi(event, context)
