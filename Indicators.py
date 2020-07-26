from math import atan
import numpy as np
import pandas as pd


def ATR(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['high']-df['low'])
    df['H-PC']=abs(df['high']-df['close'].shift(1))
    df['L-PC']=abs(df['low']-df['close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    #df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L','H-PC','L-PC'],axis=1)
    return df2


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


def o_c(ohlcv,n=33):
    df = ohlcv.copy()
    o = df['open'].rolling(window=n).mean()
    c = df['close'].rolling(window=n).mean()
    df['o_c'] = c-o
    df.dropna(inplace=True)
    return df
