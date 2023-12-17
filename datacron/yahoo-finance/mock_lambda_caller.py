import dotenv

from awslambda import lambda_get_symbols_data_multi

dotenv.load_dotenv()

event = {'time':'2023-12-17'}
context = None
lambda_get_symbols_data_multi(event, context)
