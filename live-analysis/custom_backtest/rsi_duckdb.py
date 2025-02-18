def main():
    print("Hello from custom-backtest!")

import os, sys
import pandas as pd
import duckdb as db
import matplotlib.pyplot as plt

def addrsi(df:pd.DataFrame, window = 14):
    columns = df.columns.tolist()
    col_str = "\""+"\",\"".join(columns)+"\""
    rsi = db.sql(f"""
        with stg1 as (
            select 
                *
                , Close - lag(Close,1) over (partition by Ticker order by Date asc) as c_delta
            from df 
        )
        , stg2 as (
            select 
                *
                , greatest(c_delta,0) as _u
                , abs(least(c_delta,0)) as _d
            from stg1
        ) 
        , stg3 as (
            select 
                {col_str}
                , avg(_u) over (partition by Ticker order by Date asc rows between {window} preceding and 0 following) as ua
                , avg(_d) over (partition by Ticker order by Date asc rows between {window} preceding and 0 following) as da
                , 100 * (ua)/(ua+da) as rsi_{window}
            from stg2
        )
        select 
            {col_str}
            , rsi_{window}
        from stg3
    """)
    return rsi.df()

def addrsi_signal(df:pd.DataFrame, line_name='rsi_14', buy_sig=30, sell_sig=60):
    columns = df.columns.tolist()
    col_str = "\""+"\",\"".join(columns)+"\""
    sig = db.sql(f"""
        select 
            {col_str}
            , lag({line_name},1) over (partition by Ticker order by Date asc) as last_rsi
            , case when last_rsi < {buy_sig} and {line_name} >= {buy_sig} then 1 else 0 end as buy_sig 
            , case when last_rsi < {sell_sig} and {line_name} >= {sell_sig} then 1 else 0 end as sell_sig 
        from df  
    """)
    return sig.df() 
if __name__ == "__main__":
    
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, 'orcl-1995-2014.txt')
    datapath = os.path.join(modpath, '../../datacron/yahoo-finance/localstore/daily/2000-01-01_0.parquet')
    df = db.sql(f"""
        select * from read_parquet("{datapath}")
    """).df()
    rsi = addrsi(df,14)
    cba = db.sql(f"""
        select Close, rsi_{14} 
        from rsi
        where Ticker = 'CBA.AX'
        order by Date 
    """).df()
    cba.plot()
    plt.show()
    
    # hyperparameter to test include rsi period, rsi_upper and lower cutoff signal threshold, and number of stock to monitor (perhaps this threshold should differ by instrument as well.)