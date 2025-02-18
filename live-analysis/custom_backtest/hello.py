def main():
    print("Hello from custom-backtest!")

import os, sys
import polars as pl

if __name__ == "__main__":
    
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, 'orcl-1995-2014.txt')
    datapath = os.path.join(modpath, '../../datacron/yahoo-finance/localstore/daily/2000-01-01_0.parquet')
    df = pl.read_parquet(datapath)
    
    window = 2    
    c_delta = (
        #previous
        pl.col('Close').shift(1).over(partition_by=['Ticker'],order_by='Date',descending=False) - 
        #current
        pl.col('Close')
    )
    
    U = (
        pl.when(c_delta >= 0)
        .then(c_delta)
        .otherwise(0.0)
        .rolling_mean(window_size=window)
        .over(partition_by=["Ticker"], order_by="Date", descending=False)
    )

    D = (
        pl.when(c_delta < 0)
        .then(c_delta)
        .otherwise(0.0)
        .abs()
        .rolling_mean(window_size=window)
        .over(partition_by=["Ticker"], order_by="Date", descending=False)
    )
    
    rsi = df.select(
        pl.col('Ticker'),
        pl.col('Close'),        
        U.alias('U'),
        D.alias('D'),
        100 * (U / (U + D)).alias(f'rsi_{window}')
    )
    print(rsi.filter(pl.col('Ticker') == 'CBA.AX').head(10))