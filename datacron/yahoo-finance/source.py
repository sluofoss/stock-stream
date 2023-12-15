import yfinance as yf
import yaml


class source:
    def __init__(self, symbol: str):
        self.ticker = yf.Ticker(symbol)

    def getLatestDayData(self):
        return self.tickers()

    def getDataByDay(self):
        return self.tickers()


if __name__ == "__main__":
    # s = source('MSFT', '1m')
    s = source(["BTC-AUD", "MSFT"], "1m")
    # using list for history must have multiple
    with open("config.yml", "r") as file:
        symbols = yaml.safe_load(file)
    for symbol in symbols["asx200"]:
        s = source(symbol)
        s.getLatestDayData()