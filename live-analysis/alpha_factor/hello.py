from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader as bt

import sys, datetime, os.path

def main():
    print("Hello from alpha-factor!")

if __name__ == '__main__':
    main()

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, 'orcl-1995-2014.txt')
    datapath = os.path.join(modpath, '../../datacron/yahoo-finance/localstore/daily/2000-01-01_0.parquet')

    import pandas as pd
    df = pd.read_parquet(datapath)[:100_000]
    #sd = df.rename({'Date':'datetime'})
    print(df)
    
    # Create a Data Feed
    data = bt.feeds.PandasData(
        dataname=df,
        datetime = 'Date',
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2025, 2, 13),
    )

    

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    