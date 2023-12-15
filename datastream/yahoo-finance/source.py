import yfinance as yf
from time import sleep
import datetime
import logging

now = datetime.datetime.now()


class sources:
    def __init__(self, symbols: list, interval: str):
        # len(symbols) > 1
        if len(symbols) <= 1:
            raise Exception("Not supported by yfinance lib")
        self.tickers = yf.Tickers(" ".join(symbols))
        self.__minute__ = None

    def __symbol_validator__(self):
        """
        TODO: excludes invalid symbols
        """
        for symbol_str, symbol_ticker in self.tickers.tickers.items():
            try:
                print(symbol_ticker.info)
            except Exception as e:
                print("caught exception")
                raise e

    def minute_stream(self):
        """
        TODO: test whether the newest minute data is the current incomplete, or last completed
        """
        self.__minute__ = datetime.datetime.now().replace(second=0, microsecond=0)
        while True:
            sleep(1)
            now = datetime.datetime.now()
            now_minute = now.replace(second=0, microsecond=0)
            if now_minute != self.__minute__:
                sleep(5)
                self.__minute__ = now_minute
                # output =
                print()
                print(self.tickers.history(period="1d", interval="1m"))
                # TODO: extract and emit only the latest data that is not seen before?


class source:
    def __init__(self, symbol: str):
        pass


if __name__ == "__main__":
    # s = source('MSFT', '1m')
    s = sources(["BTC-AUD", "MSFT"], "1m")
    # using list for history must have multip
    s.__symbol_validator__()
    s.minute_stream()
