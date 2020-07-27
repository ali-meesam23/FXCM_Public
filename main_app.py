from initialize import initialize_connection as con
from  ohlcv import interval, ohlcv
from Signal import signal

# Basic Imports
import datetime
import time
# =====================imput parameters=====================

# Trading pairs
tickers = {
    'EUR/USD':30,
    'XAU/USD':10,
    'US30':20,
    'AUD/USD':30,
    'GBP/USD':30,
    'USD/CAD':30
}

# trading time
s_time = datetime.time(6,30)
e_time = datetime.time(16)
now = datetime.datetime.now().time()

# Trading interval
trade_interval = interval.oneMinute
trade_interval_refresh = 60 * 1
# Activating the algorithm for the active time range
activation_condition = ((s_time < now) and (now < e_time))

# ===========================================================

while activation_condition==True:

    account = con.get_accounts()
    balance = account.balance
    positions = con.get_open_positions()
    perc_total_balance = 0.9


    for ticker in tickers:
        # ======= Getting data ===========
        df = ohlcv(ticker,trade_interval)
        
        # ======== Position sizing ========
        con.subscribe_market_data(ticker)
        price = con.get_last_price(ticker).mean()
        con.unsubscribe_market_data(ticker)
        total_borrow_amount = ((perc_total_balance*balance.iloc[0]/len(tickers))*tickers[ticker])
        # Order amount
        order_amount = round(total_borrow_amount/price,0)
        
        if (len(ticker)==7) and (ticker!="XAU/USD"):
            order_amount = order_amount/1000    
        
        if order_amount==0:
            order_amount += 1
        # =================================
        
        # ======== Signal ==========
        s_ticker = signal(df)
        
        is_Buy = None
        try:
            is_Buy = positions.loc[positions.currency==ticker,"isBuy"].iloc[0]
        except:
            print(f"No open position for {ticker}")
        
        # BUYING
        if s_ticker == 1 and ((is_Buy is None) or (is_Buy==False)):
            # Closing the short position
            if is_Buy == False:
                con.close_all_for_symbol(ticker)
                print(f"CLOSING POSITION for {ticker}")
            # buy order
            try:
                con.create_market_buy_order(ticker, order_amount)
                print(f"Created BUY order for {ticker}: {order_amount}")
            except:
                print(f"Buy Order failed for {ticker}")
                
        # SHORTING  
        elif s_ticker == -1 and ((is_Buy is None) or (is_Buy == True)):
            # Closing the long position
            if is_Buy == True:
                con.close_all_for_symbol(ticker)
                print(f"CLOSING POSITION for {ticker}")
            # sell order
            try:
                con.create_market_sell_order(ticker, order_amount)
                print(f"Created SELL order for {ticker}: {order_amount}")
            except:
                print(f"Sell Order failed for {ticker}")
                
        # CLOSING 
        elif s_ticker == 0 and (is_Buy is not None):
            # close the position
            con.close_all_for_symbol(ticker)
            print(f"CLOSING POSITION for {ticker}")
        else:
            print(f"No new positions open for {ticker}...")

    if activation_condition==True:
        print()
        print(f"Current PnL: {round(con.get_accounts().dayPL.iloc[0],0)}")
        time.sleep(trade_interval_refresh)

print("Trading session over....")
print("_________________________")
print("Closing All Trades")

active_pos = con.get_open_positions()
if len(active_pos)>0:
    for ticker in tickers:
        try:
            con.close_all_for_symbol(ticker)
            print(f"Closed trade for {ticker}...")
        except:
            print(f"No position available for {ticker}")
else:
    print('No Positions to Close')

con.close()
