import yfinance as yf
#query = yf.EquityQuery('and',[
#    yf.EquityQuery('is-in',['exchange', 'ASX'])
#])

query = yf.EquityQuery('is-in',['exchange', 'ASX'])
import json
#
res = yf.screen(query, size=1)
total = res['total']
res['quotes']=[]
for offset in range(0,total,100):
    res['quotes'] += yf.screen(query, size=100, offset=offset, sortField='intradaymarketcap', sortAsc=False)['quotes']

res['symbols'] = [x['symbol'] for x in res['quotes']]
#print(len(res['symbols']))

print(json.dumps(res,indent=4))

#print(yf.Ticker('AX.CBA').history())