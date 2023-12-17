import boto3
import os
import concurrent.futures
import datetime
from source import Source


def check_symbol_info(symbol):
    s = Source(symbol)
    return s.ticker.info


def lambda_get_symbols_data_multi(event, context):
    """takes the current date from context and get entire day of data
    use case when schedule on a market after market closes

    Args:
        event (_type_): _description_
        context (_type_): _description_
    """
    print(event)
    print(context)
    import pandas as pd

    df = pd.read_csv("./ASX_Listed_Companies_17-12-2023_01-39-05_AEDT.csv")
    # print(df)
    symbols = [x + ".AX" for x in df["ASX code"]]

    get_symbols_data_multi(
        symbols,
        max_worker=50,
        s3_save_bucket=os.getenv("S3_STORE_BUCKET"),
        local_save = True, # TODO: remove this 
        exec_date=event["time"],  # TODO: Confirm this
    )


def get_symbols_data_multi(
    symbols,
    max_worker=10,
    print_data=False,
    local_save: str = None,
    s3_save_bucket: str = None,
    exec_date=None,
):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
        if exec_date is None:
            future_to_symbol = {
                executor.submit(Source(symbol).getLatestDayData): symbol
                for symbol in symbols
            }
            exec_date = datetime.date.today()
            print("Today's date:", exec_date)
        else:
            next_day = datetime.datetime.strptime(
                exec_date, "%Y-%m-%d"
            ) + datetime.timedelta(days=1)
            future_to_symbol = {
                executor.submit(
                    Source(symbol).getDataByDate, exec_date, next_day
                ): symbol
                for symbol in symbols
            }
            print(f"Get Data on Date {exec_date} before {next_day}")

        print("created future", flush=True)
        for future in future_to_symbol:
            symbol = future_to_symbol[future]
            try:
                data = future.result()
            except Exception as exc:
                print("%r generated an exception: %s" % (symbol, exc), flush=True)
            else:
                print(
                    "%r Symbol is successful with len %d" % (symbol, len(data)),
                    flush=True,
                )
                if print_data:
                    print(data)
                if local_save:
                    if not os.path.exists(f"./mocks3yfinance/{symbol}/"):       
                        os.makedirs(f"./mocks3yfinance/{symbol}/") 
                    data.to_parquet(
                        #f"./mocks3yfiance/{symbol}/{exec_date}.parquet.gzip"
                        f"./mocks3yfinance/{symbol}/{exec_date}.parquet",
                        compression="gzip",
                    )
                if s3_save_bucket:
                    pass
                    # TODO

def check_symbols_info_multi(symbols, max_worker=10, print_data=False):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
        future_to_symbol = {
            executor.submit(check_symbol_info, symbol): symbol for symbol in symbols
        }
        print("created future", flush=True)
        for future in future_to_symbol:
            symbol = future_to_symbol[future]
            try:
                data = future.result()
            except Exception as exc:
                print("%r generated an exception: %s" % (symbol, exc), flush=True)
            else:
                pass
                print(
                    "%r Symbol is successful with len %d" % (symbol, len(data)),
                    flush=True,
                )
                if print_data:
                    print(data)


def check_symbol_info_loop(symbols):
    data_store = {}
    except_store = {}
    for i, symbol in enumerate(symbols):
        s = Source(symbol)
        try:
            data_store[symbol] = s.ticker.info
            print(i, symbol, "success", flush=True)
        except Exception as e:
            print(i, e, flush=True)
            except_store[symbol] = str(e)
