import boto3

import os, yaml
import concurrent.futures

from source import Source


def check_symbol_info(symbol):
    s = Source(symbol)
    return s.ticker.info

def get_symbols_data_multi(symbols, max_worker=10):
    curr_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(curr_path, "symbols.yml"), "r") as file:
        symbols = yaml.safe_load(file)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
        future_to_symbol = {
            executor.submit(Source(symbol).getLatestDayData): symbol for symbol in symbols["asx200"]
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
                print("%r Symbol is successful with len %d" % (symbol, len(data)), flush=True)
                #print(data)
def check_symbols_info_multi(max_worker=10):
    curr_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(curr_path, "symbols.yml"), "r") as file:
        symbols = yaml.safe_load(file)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
        future_to_symbol = {
            executor.submit(check_symbol_info, symbol): symbol for symbol in symbols["asx200"]
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
                print("%r Symbol is successful with len %d" % (symbol, len(data)), flush=True)
def check_symbol_info_loop():
    curr_path = os.path.abspath(os.path.dirname(__file__))
    # s = source('MSFT', '1m')
    # using list for history must have multiple
    with open(os.path.join(curr_path, "symbols.yml"), "r") as file:
        symbols = yaml.safe_load(file)
    print("finished loading symbols", flush=True)
    data_store = {}
    except_store = {}
    for i, symbol in enumerate(symbols["asx200"]):
        s = Source(symbol)
        try:
            data_store[symbol] = s.ticker.info
            print(i, symbol, "success", flush=True)
        except Exception as e:
            print(i, e, flush=True)
            except_store[symbol] = str(e)

if __name__ == '__main__':
    pass