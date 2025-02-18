import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

import sys, datetime, os.path
import numpy as np
import pandas as pd


frames = []
for feed in range(1,2+1):
    # Define the date range
    date_range = pd.date_range(start='2015-01-01', end='2021-01-01', freq='B')  # 'B' stands for business days (weekdays)

    # Define the time range for each day
    time_range = pd.date_range(start='08:00', end='17:00', freq='min').time  # 'T' stands for minute frequency

    # Generate the datetime index by combining date and time
    #datetime_index = pd.MultiIndex.from_product([date_range, time_range], names=['Date', 'Time'])
    #datetime_index = [pd.Timestamp.combine(date, time) for date, time in datetime_index]

    # Create the DataFrame
    #df = pd.DataFrame(index=datetime_index)
    df = pd.DataFrame(index=date_range)
    #df['Minute'] = [dt.minute for dt in df.index]  # Example column

    for col in "Open High Low Close Volume".split():
        for s in range(2,10):
            df[col+' '*(s-2)] = s*feed/2+ np.arange(df.shape[0])**2
    frames.append(df)
    #print(df)
#print(date_range)

#print(time_range)

#print(df.shape)

import time

def track_time(t):
    new_t = time.time()
    print(new_t - t)
    return new_t

class MyStrategy(bt.Strategy):
    
    def __init__(self):
        #print(len(self.datas))
        #(maybe calc using open and purchase using high?)
        #(or calc using close and purchase using slippage)
        self.rsis = [
            btind.RSI_EMA(feed, period = 14) 
            #bt.talib.RSI(feed)
            for feed in self.datas
        ]
    def next(self):
        print(self.rsis[0][0])

if __name__ == '__main__':
    t = time.time()
    
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    
    # Create a Data Feed
    for df in frames:
        data = bt.feeds.PandasData(
            dataname=df,
            datetime = None,#'Date',
            # Do not pass values before this date
            fromdate=datetime.datetime(2015, 1, 1),
            # Do not pass values after this date
            todate=datetime.datetime(2021, 1, 1),
            )


        t = track_time(t)

        # Add the Data Feed to Cerebro
        cerebro.adddata(data)
    
    t = track_time(t)

    # add strategy
    cerebro.addstrategy(MyStrategy)

    # Set our desired cash start
    cerebro.broker.setcash(100_000.0)

    t = track_time(t)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    t = track_time(t)

    # Run over everything
    cerebro.run()

    t = track_time(t)

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    t = track_time(t)
    