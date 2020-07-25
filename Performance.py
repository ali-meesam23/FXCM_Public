from timeit import default_timer as timer
start = timer()


from initialize import con
d1 = timer()-start
print('D1: ',d1)
start = timer()

from ohlcv import ohlcv,interval
d2 = timer()-start
print('D2: ',d2)
start = timer()
# performace Test

ohlcv(ticker='EUR/USD', period=interval.fifteenMinute, ticks=250)
d3 = timer()-start
print('D3: ',d3)
start = timer()

ohlcv(ticker='GBP/USD', period=interval.fifteenMinute, ticks=250)
d4 = timer()-start
print('D4: ',d4)
start = timer()


con.close()
d5 = timer()-start
print('D5: ',d5)
