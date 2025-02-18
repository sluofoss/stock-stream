def main():
    print("Hello from custom-backtest!")

import os, sys
import polars as pl

if __name__ == "__main__":
    
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, 'orcl-1995-2014.txt')
    datapath = os.path.join(modpath, '../../datacron/yahoo-finance/localstore/daily/2000-01-01_0.parquet')
    df = pl.read_parquet(datapath)
    with pl.SQLContext(register_globals=True) as ctx:
        res = ctx.execute("""
            with ctx as (
                select 
                    Date, Ticker, "Adj Close", "Close", "Dividends", "High", "Low", "Open", "Stock Splits", "Volume"
                    , lag(Close, 1) over (partition by Ticker order by Date) 
                from df
            )
            select *
            from ctx 
        """)
        print(res)#.collect())