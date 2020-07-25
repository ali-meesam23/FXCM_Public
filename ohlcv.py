from initialize import con


class Period:
    def __init__(self):
        self.oneMinute = 'm1'
        self.fiveMinute = 'm5'
        self.fifteenMinute = 'm15'
        self.thirtyMinute = 'm30'
        self.oneHour = 'H1'
        self.twoHour = 'H2'
        self.threeHour = 'H3'
        self.fourHour = 'H4'
        self.sixHour = 'H6'
        self.eightHour = 'H8'
        self.oneDay = 'D1'
        self.oneWeek = 'W1'
        self.oneMonth = 'M1'


interval = Period()


def ohlcv(ticker, period=interval.oneMinute, ticks=50):

    df = con.get_candles(ticker, period=period, number=ticks)
    o = 'open'
    h = 'high'
    l = 'low'
    c = 'close'
    df[o] = (df[f'bid{o}']+df[f'ask{o}'])/2
    df[h] = (df[f'bid{h}']+df[f'ask{h}'])/2
    df[l] = (df[f'bid{l}']+df[f'ask{l}'])/2
    df[c] = (df[f'bid{c}']+df[f'ask{c}'])/2
    df.drop(df.columns[[0, 1, 2, 3, 4, 5, 6, 7]], axis=1, inplace=True)
    df.rename(columns={'tickqty': 'vol'}, inplace=True)
    return df

