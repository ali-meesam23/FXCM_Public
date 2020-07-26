from ohlcv import ohlcv, interval
from Indicators import vwap_slope, o_c

import pandas as pd
import numpy as np

def signal(ticker_ohlcv_data):
    df = ticker_ohlcv_data.copy()
    
    df = vwap_slope(df)
    df = o_c(df)

    df['v_s'] = df['VWAP_Slope'].apply(lambda x: 1 if x>0 else 0)
    df['o_s'] = df['o_c'].apply(lambda x: 1 if x>0 else 0)

    df['sell'] = np.where(((df['v_s']==0) & (df['o_s']==0)),-1,0)
    df['buy'] = np.where(((df['v_s']==1) & (df['o_s']==1)),1,0)
    df['signal'] = np.where(((df.sell==-1)|((df.sell==0)&(df.buy==0))),df.sell,df.buy)

    return df['signal'].iloc[-1]
