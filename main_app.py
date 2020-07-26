from initialize import initialize_connection as con

# Basic Imports
import datetime

# =====================imput parameters=====================

# Trading pairs
target_pairs = {
    'EUR/USD':30,
    'XAU/USD':10,
    'US30':20,
    'AUD/USD':30,
    'GBP/USD':30,
    'USD/CAD':30
}

# trading time
s_time = datetime.time(7)
e_time = datetime.time(17)
now = datetime.datetime.now().time()

# Activating the algorithm for the active time range
activation_condition = s_time<=now and now<=e_time

# Account information
account = con.get_accounts()
balance = account.balance
dayPL = account.dayPL

# Equity per ticker
available_equtity_per_ticker = balance/len(target_pairs)*(target_pairs['EUR/USD'])*0.5

# Open Positions
open_positions = con.get_open_positions()

# ===========================================================

while activation_condition:
    pass
