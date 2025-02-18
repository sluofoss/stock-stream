there are some backtesting framework out there but none of them fits my need to backtest multiple stocks at once. 
- backtrader is slow as hell. I tried passing in 400 stocks for data between 2000 and 2020, and it never finished passing the dataframe.
- zipline 
- backtrader
- pyalgotrade
- bt
- lean
- finmarketpy
- vnpy



the amount of time with no next in strategy is proportional to number of feeds and length of dataframe.

6 years and  20 feed is  5 seconds
6 years and 100 feed is 22 seconds
6 years and 400 feed is 93 seconds
