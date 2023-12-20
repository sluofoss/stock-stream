import dotenv

from awslambda import lambda_get_symbols_data_multi, lambda_check_symbols_info_multi

dotenv.load_dotenv()


event = {'time':'2023-12-14'}
context = None
lambda_get_symbols_data_multi(event, context)
#lambda_check_symbols_info_multi(event, context)