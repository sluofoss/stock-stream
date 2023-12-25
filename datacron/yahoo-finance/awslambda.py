import boto3
import os
import concurrent.futures
import datetime
from source import Source
import logging.config
import yaml
import sys
import yfinance as yf

logger = logging.getLogger("lambda")
logger.info("awslambda.PY is here!!!!")
logger = logging.getLogger("lambda")
with open("logconfig.yaml", "r") as configfile:
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
    logger.info(event)
    logger.info(context)

    import pandas as pd

    df = pd.read_csv("./ASX_Listed_Companies_17-12-2023_01-39-05_AEDT.csv")
    # print(df)
    symbols = [x + ".AX" for x in df["ASX code"]]

    start_date = event["time"]  # TODO: Confirm this
    next_day = datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(
        days=1
    )

    get_symbols_data_multi(
        symbols,
        max_worker=50,
        s3_save_bucket=os.getenv("S3_STORE_BUCKET"),
        local_save=True,  # TODO: remove this
        yf_hist_arg={"start": start_date, "end": next_day, "interval": "1m"},
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

    import pandas as pd

    df = pd.read_csv("./ASX_Listed_Companies_17-12-2023_01-39-05_AEDT.csv")
    # print(df)
    symbols = [x + ".AX" for x in df["ASX code"]]

    check_symbols_info_multi(symbols, max_worker=50, print_data=True)


def get_symbols_data_multi(
    symbols,
    max_worker=10,
    print_data=False,
    local_save: str = None,
    s3_save_bucket: str = None,
    s3_parent_key="yfinance/min",
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
                if local_save:
                    logger.info(f"{symbol}:Saving to local")
                    if not os.path.exists(f"./mocks3yfinance/{symbol}/"):
                        os.makedirs(f"./mocks3yfinance/{symbol}/")
                    data.to_parquet(
                        # f"./mocks3yfinance/{symbol}/{exec_date}.parquet.gzip"
                        f"./mocks3yfinance/{symbol}/{yf_hist_args.get('start',datetime.date.today())}.parquet",
                        compression="gzip",
                    )
                if s3_save_bucket:
                    logger.info(f"{symbol}: Saving to s3")
                    data.to_parquet(
                        # f"./mocks3yfinance/{symbol}/{exec_date}.parquet.gzip"
                        f"s3://{s3_save_bucket}/{s3_parent_key}/{symbol}/{yf_hist_args.get('start',datetime.date.today())}.parquet",
                        compression="gzip",
                    )


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
        s = Source(symbol)
        try:
            data_store[symbol] = s.ticker.info
            logger.info(f"{i}, {symbol}, success")
        except Exception as e:
            logger.info(f"{i}, {e}")
            except_store[symbol] = str(e)
