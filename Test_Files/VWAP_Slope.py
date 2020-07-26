from initialize import con
from ohlcv import interval, ohlcv
import pandas as pd
from math import atan


def VWAP(ohlcv):
    df = ohlcv.copy()
    df['cumVol'] = df['vol'].cumsum()
    df['cum_ohc3Vol'] = (((df[['open','high','close']].sum(axis=1))/3)*df['vol']).cumsum()
    df['VWAP'] = df['cum_ohc3Vol']/df['cumVol']
    df.drop(df.columns[[5,6]],axis=1,inplace=True)
    return df


def slope(df,col,n):
    """
    n = bars back
    """
    df = df.copy()
    ser = df[col]
    slp = []
    for i,x in enumerate(ser):
        if i < n:
            slp.append(0)
            continue
        #getting values to find the slope
        b = ser[i]
        a = ser[i-n]
        slope = atan((b-a)/n)
        slp.append(slope)
    df[f'{col}_Slope'] = pd.Series(slp,index=df.index)
    return df


def vwap_slope(ohlcv_data):
    df = ohlcv_data.copy()
    df = VWAP(df)
    df = slope(df,'VWAP',3)
    return df


print(vwap_slope(ohlcv('EUR/USD',period=interval.fiveMinute,ticks=250)))

con.close()