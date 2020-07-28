from initialize import initialize_connection as con
from ohlcv import interval, ohlcv
from Signal import signal

# Basic Imports
import datetime
import time
import sqlite3
# =====================imput parameters=====================

# Trading pairs


 #   'XAU/USD':10,
  #  'US30':20,
   # 'AUD/USD':30,
    #'GBP/USD':30,

tickers = {
    'EUR/USD':30,
    'GBP/USD':30,
    'USD/CAD':30
}

# trading times
start = input("Enter a start time HH:MM (24h.): ")
end = input("Enter an end time HH:MM (24h.: ")
s = start.split(":")
e = end.split(":")
if len(s)==2:
    s_time = datetime.time(int(s[0]),int(s[1]))
else:
    s_time = datetime.time(7, 30)
if len(e)==2:
    e_time = datetime.time(int(e[0]),int(e[1]))
else:
    e_time = datetime.time(14, 30)

now = datetime.datetime.now().time()

# Trading interval
trade_interval = interval.fifteenMinute
trade_interval_refresh = 60 * 15
# Activating the algorithm for the active time range
activation_condition = ((s_time < now) and (now < e_time))

# ===========================================================
# RECORDING SESSION PNL
db_name = 'orders_pnl.db'
connection = sqlite3.connect(db_name)
cursor = connection.cursor()


while activation_condition==True:

    account = con.get_accounts()
    balance = account.balance
    positions = con.get_open_positions()
    perc_total_balance = 0.8


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
        
        # ___TP and SL in pips___
        take_profit = 80
        stop_loss = -20

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
                con.open_trade(symbol=ticker, is_buy=True,
                       is_in_pips=True,
                       amount=order_amount, 
                       order_type='AtMarket',
                       time_in_force='GTC',
                       limit=take_profit,
                       stop=stop_loss,
                       trailing_step =True
                       )
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
                con.open_trade(symbol=ticker, is_buy=False,
                       is_in_pips=True,
                       amount=order_amount, 
                       order_type='AtMarket',
                       time_in_force='GTC',
                       limit=take_profit,
                       stop=stop_loss,
                       trailing_step =True
                       )
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
    
    now = datetime.datetime.now().time()
    activation_condition = ((s_time < now) and (now < e_time))

    if activation_condition:
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pnl = round(con.get_accounts().dayPL.iloc[0],0)
        insert_into = f"INSERT INTO pnl (time,PnL) VALUES (?,?)"
        cursor.execute(insert_into,(time_stamp,pnl))
        connection.commit()
        print()
        print(f"Current PnL: {pnl}")
        time.sleep(trade_interval_refresh)

# Saving and Closing DB

connection.close()

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
print("Connection Closed...")