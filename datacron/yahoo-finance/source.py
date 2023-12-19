import yfinance as yf
import yaml

import enum
import logging

logger = logging.getLogger("lambda")
#logger.propagate = True
logger.info("SOURCE.PY is here!!!!")
class PERIOD(enum.Enum):
    d1 = "1d"
    d5 = "5d"
    m1 = "1mo"
    m3 = "3mo"
    m6 = "6mo"
    y1 = "1y"
    y2 = "2y"
    y5 = "5y"
    y10 = "10y"
    ytd = "ytd"
    max = "max"


class Source:
    def __init__(self, symbol: str):
        self.ticker = yf.Ticker(symbol)

    def getLatestDayData(self):
        return self.ticker.history(period="1d", interval="1m")

    def getDataByPeriod(self, period: PERIOD):
        return self.ticker.history(period=period, interval="1m")

    def getDataByDate(self, start_date, end_date):
        return self.ticker.history(start=start_date, end=end_date, interval="1m")


if __name__ == "__main__":
    import os

    curr_path = os.path.abspath(os.path.dirname(__file__))
    # s = source('MSFT', '1m')
    # using list for history must have multiple
    with open(os.path.join(curr_path, "symbols.yml"), "r") as file:
        symbols = yaml.safe_load(file)
    logger.info("finished loading symbols")
    data_store = {}
    except_store = {}
    for i, symbol in enumerate(symbols["asx200"]):
        s = Source(symbol)
        try:
            data_store[symbol] = s.ticker.info
            logger.info(f"{i}, {symbol}, success")
        except Exception as e:
            logger.error(f"{i}, {e}")
            except_store[symbol] = str(e)
    import json

    with open(os.path.join(curr_path, "symbol_info"), "w") as file:
        json.dump(data_store, file)
    with open(os.path.join(curr_path, "symbol_failed"), "w") as file:
        json.dump(except_store, file)
