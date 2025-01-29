"""
Collection of functions to be executed in the AWS environment to retrieve data from yahoo finance.

Env Var:
    env: 
        determine which environment code is executed in.
        valid: local, dev, uat, prod
    YF_HIST_ARG:
        [Optional] json string parametrizing the yfinance.Ticker.History method
    LOCAL_SAVE_PATH:
        [Optional] determines if the result should be stored on local machine. useful outside of lambda 
        (i.e. in container env or local exec) 
    S3_STORE_BUCKET:
        [Optional] bucket name to store result
    S3_STORE_PARENT_KEY:
        [Optional] root key in s3 bucket to store result.
"""
import os, json, datetime, sys
import concurrent.futures
import logging.config

#import boto3
import io
import yaml
import yfinance as yf
import pandas as pd

logger = logging.getLogger("lambda")
logger.info("awslambda.PY is here!!!!")
logger = logging.getLogger("lambda")

if os.getenv("env") == "local": #TODO: figure out how to change this for dev, uat, prod
    cfg_file_name = "logconfig.yaml"
else:
    cfg_file_name = "logconfig_aws.yaml"
print(cfg_file_name)
with open(cfg_file_name, "r") as configfile:
    configdict = yaml.safe_load(configfile)
    logging.config.dictConfig(configdict)

# logger.setLevel(logging.DEBUG)
# h = logging.FileHandler('./lambda.log')
# h.setLevel(logging.DEBUG)
# logger.addHandler(h)
# logger.info("mock started")

# logging.getLogger('yfinance').addHandler(logging.FileHandler('./lambda.log'))
# logger.propagate = True


def lambda_get_symbols_data_multi(event, context):
    """takes the current date from context and get entire day of data
    use case when schedule on a market after market closes

    Args:
        event (_type_): _description_
        context (_type_): _description_
    """
    logger.info(f"event:{event}")
    logger.info(f"context:{context}")


    df = pd.read_csv("./ASX_Listed_Companies_30-01-2025_02-54-26_AEDT.csv")
    # print(df)
    symbols = [x + ".AX" for x in df["ASX code"]]

    # Event time looks like 2024-01-26T08:12:00Z
    # TODO: decide whether need to adjust this for other markets deployed in other aws regions
    start_date = datetime.datetime.strptime(
        event["time"], "%Y-%m-%dT%H:%M:%S%z"
    ).astimezone(tz=None).date()
    next_day = start_date + datetime.timedelta(days=1)
    __exec_time_zone = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo
    logger.info(f"start_date: {start_date}, next_day: {next_day}, exec_time_zone: {__exec_time_zone}")
    
    # TODO: add with try except
    if os.getenv("YF_HIST_ARG") is None:
        # lambda event with predefined interval
        yf_hist_args = {"start": start_date, "end": next_day, "interval": "1m"}
    else:
        # custom load 
        yf_hist_args = json.loads(os.getenv("YF_HIST_ARG"))
        yf_hist_args['start'] = yf_hist_args.get('start',datetime.date.today())

    get_symbols_data_multi_combined(
        symbols,
        max_worker=int(os.getenv('WORKER_NUM', 50)),
        print_data=bool(os.getenv('PRINT_DATA_IN_LOG', False)),
        local_save_path=os.getenv("LOCAL_SAVE_PATH"),  # TODO: remove this
        s3_save_bucket=os.getenv("S3_STORE_BUCKET"),
        s3_parent_key=os.getenv("S3_STORE_PARENT_KEY"),
        yf_hist_args=yf_hist_args,
    )


def lambda_check_symbols_info_multi(event, context):
    """check symbol info
    use case: validate asx symbol consistent in yfinance

    Args:
        event (_type_): _description_
        context (_type_): _description_
    """
    logger.info(event)
    logger.info(context)


    df = pd.read_csv("./ASX_Listed_Companies_30-01-2025_02-54-26_AEDT.csv")
    # print(df)
    symbols = [x + ".AX" for x in df["ASX code"]]

    check_symbols_info_multi(symbols, max_worker=50, print_data=True)


def get_symbols_data_multi_combined(
    symbols,
    max_worker=10,
    print_data=False,
    local_save_path: str = None,
    s3_save_bucket: str = None,
    s3_parent_key: str = None,
    yf_hist_args: dict = {"interval": "1m"}, #TODO doesnt work on its own right now
):
    # this method stores all the tickers inside 1 folder for ease of sql querying with athena and spark.
    print("yfinance param")
    print(yf_hist_args)
    try:
        #['CBA.AX','WOW.AX']
        data = yf.Tickers(symbols).history(**yf_hist_args), 
    except Exception as exc:
        logger.error(f"combined run generated an exception: {exc}")
    else:
        print(data)
        print(type(data[0]))
    
        data = data[0].stack(level=1).reset_index()
        
        if data.isnull().all(axis=1).all():
            raise ValueError("The DataFrame contains only rows with null values.")
    
        if local_save_path:
            logger.info(f"{yf_hist_args['start']}:Saving to local")
            if not os.path.exists(f"./{local_save_path}/"):
                os.makedirs(f"./{local_save_path}/")
            data.to_parquet(
                f"./{local_save_path}/{yf_hist_args['start']}.parquet",
                #compression="gzip", snappy better for read, gzip for cold data
            )
        if s3_save_bucket:
            logger.info(f"{yf_hist_args['start']}: Saving to s3")
            data.to_parquet(
                f"s3://{s3_save_bucket}/{s3_parent_key}/{yf_hist_args['start']}.parquet",
            )

def get_symbols_data_multi(
    symbols,
    max_worker=10,
    print_data=False,
    local_save_path: str = None,
    s3_save_bucket: str = None,
    s3_parent_key: str = None,
    yf_hist_args: dict = {"interval": "1m"},
):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
        logger.info(f"yfinance receiving arguments: {yf_hist_args}")

        future_to_symbol = {
            executor.submit(
                lambda kwargs: yf.Ticker(symbol).history(**kwargs), yf_hist_args
            ): symbol
            for symbol in symbols
        }

        logger.info("created future")

        for future in future_to_symbol:
            symbol = future_to_symbol[future]
            # print("symbol format is weird: ", symbol, flush=True)
            try:
                data = future.result()
            except Exception as exc:
                logger.error(f"{symbol} generated an exception: {exc}")
            else:
                logger.info(
                    f"{symbol} Symbol request is successful with len {len(data)}"
                )
                if print_data:
                    logger.info(f"{symbol}: {data}")
                if local_save_path:
                    logger.info(f"{symbol}:Saving to local")
                    if not os.path.exists(f"./{local_save_path}/{symbol}/"):
                        os.makedirs(f"./{local_save_path}/{symbol}/")
                    data.to_parquet(
                        f"./{local_save_path}/{symbol}/{yf_hist_args['start']}.parquet",
                    )
                if s3_save_bucket:
                    logger.info(f"{symbol}: Saving to s3")
                    data.to_parquet(
                        f"s3://{s3_save_bucket}/{s3_parent_key}/{symbol}/{yf_hist_args['start']}.parquet",
                    )

def boto_save_csv(df, s3_client, s3_bucket, s3_key):
    logger.info("enter my boto func")
    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)
        logger.info("to csv buffer done")

        response = s3_client.put_object(
            Bucket=s3_bucket, Key=s3_key, Body=csv_buffer.getvalue()
        )
        logger.info("put to s3")

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status == 200:
            print(f"Successful S3 put_object response. Status - {status}")
        else:
            print(f"Unsuccessful S3 put_object response. Status - {status}")

def check_symbols_info_multi(symbols, max_worker=10, print_data=False):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
        future_to_symbol = {
            executor.submit(
                lambda symbol: yf.Ticker(symbol).ticker.info, symbol
            ): symbol
            for symbol in symbols
        }
        logger.info("created future")
        for future in future_to_symbol:
            symbol = future_to_symbol[future]
            try:
                data = future.result()
            except Exception as exc:
                logger.error(f"{symbol} generated an exception: {exc}")
            else:
                logger.info(
                    f"{symbol} Symbol request is successful with len {len(data)}"
                )
                if print_data:
                    logger.info(data)


def check_symbol_info_loop(symbols):
    data_store = {}
    except_store = {}
    for i, symbol in enumerate(symbols):
        s = yf.Ticker(symbol)
        try:
            data_store[symbol] = s.ticker.info
            logger.info(f"{i}, {symbol}, success")
        except Exception as e:
            logger.info(f"{i}, {e}")
            except_store[symbol] = str(e)
