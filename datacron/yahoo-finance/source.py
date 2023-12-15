import yfinance as yf
import yaml

import enum


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


class source:
    def __init__(self, symbol: str):
        self.ticker = yf.Ticker(symbol)

    def getLatestDayData(self):
        return self.ticker.history(period="1d", interval="1m")

    def getDataByPeriod(self, period: PERIOD):
        return self.ticker.history(period=period, interval="1m")

    def getDataByDate(self, start_date, end_date):
        return self.ticker.history(start=start_date, end=end_date, interval="1m")


if __name__ == "__main__":
    # s = source('MSFT', '1m')
    s = source(["BTC-AUD", "MSFT"], "1m")
    # using list for history must have multiple
    with open("config.yml", "r") as file:
        symbols = yaml.safe_load(file)
    for symbol in symbols["asx200"]:
        s = source(symbol)
        s.getLatestDayData()
