#!/usr/bin/python3
import cbpro, json, requests, sys
import os.path
from time import sleep
from datetime import datetime
import config as conf
from send_email import email
import dcabot_logging

# main.py
# k.i.s.s. (LOL)
# should ingest what and how much crypto to buy, make the trade, handle results.

# It'd be nice to load this from a file, somehow

# DCA profile, dcabot keyname
#SECRET_B64 = 'd3p3VWp1ZG6WtRslLoIbggJxl7QNJQzjm4XvrQ9n9rziXrG6ZjBiCzkGD07O3nYXpqrXOCHVDzOq/vDW9X2m2g=='
#API_KEY = '3b5ac500a3545f9515439cc242fbcdb1'
#KEY_PASS = 'wkwjycgzm8'

class Order(object):
    def __init__(self, currency, amount, tx_id=None):
        self.currency = currency
        self.amount = amount
        self.tx_timestamp = str(datetime.now())
        self.tx_id = tx_id
        self.tx_placed = False
        self.tx_confirmed = False
        self.message = ""


def place_buy(auth_client, currency, amount):
    currency = currency.upper()
    amount = float(amount)
    order_details = auth_client.place_market_order(product_id=currency,
            side='buy',
            funds=amount)
    if "id" in order_details:
        print(f"Order placed for ${amount:.2f} of {currency}.")
        sleep(0.05)
        receipt = confirm_order(auth_client, order_details['id'])
        if ('message' in receipt):
            print(f"ERROR: {receipt['message']}")
        else:
            print(f"DEBUG: {currency} order details:\n" + json.dumps(order_details, indent=2))
            return order_details
    else:

        print(f"Order for ${amount:.2f} of {currency} was never placed (You have not been charged).")
        print(f"message:\n>{order_details['message']}")
        return order_details['message']

def confirm_order(auth_client, order_id):
    o = auth_client.get_order(order_id)
    if 'message' in o:
        print(f"ERROR: There was a problem confirming order {order_id}")
        return o
    print(f"INFO: Confirmed order {o['product_id']} for ${float(o['funds']):.2f} (Fee: ${float(o['fill_fees']):.4f}).")
    return o


def main():
    conf.check_files_exist()
    
    tracked_currencies = conf.get_tracked_currencies()
    api_key = conf.api_key
    api_secret = conf.api_secret
    api_password = conf.api_password

    threshold_daily_buy = conf.threshold_daily_buy
    btcusd_daily_buy = conf.btcusd_daily_buy
    ethusd_daily_buy = conf.ethusd_daily_buy
    total_sought_usd = btcusd_daily_buy + ethusd_daily_buy

    usd_balance = 0.0
    
    print("INFO: Starting client...")
    auth_client = cbpro.AuthenticatedClient(
            key=api_key,
            b64secret=api_secret,
            passphrase=api_password)  
    all_accounts = auth_client.get_accounts()
    
    tracked_currencies = conf.get_tracked_currencies()
    
    for acct in all_accounts:
        if (acct['currency'] == "USD"):
            usd_balance = float(acct['balance'])

    print(f'DEBUG: Avalable balance to trade: ${usd_balance:.2f}')

    if (usd_balance > threshold_daily_buy):
        if (usd_balance < total_sought_usd):
            print(f"ERROR: Insufficient funds to buy! \nUSD balance:\t${usd_balance}\nTotal sought:\t${total_sought_usd:.2f}")
            # email(fail_msg)
            exit(1)
        tracked_currencies = conf.get_tracked_currencies()
        for curr_amt_pair in tracked_currencies:
            place_buy(auth_client, curr_amt_pair[0], curr_amt_pair[1])

            
    else:
        print(f"ERROR: Insufficient funds! (balance: ${usd_balance:.2f}, threshold balance: ${threshold_daily_buy:.2f})")
        email_message = """
Sup,
Your daily trade was not executed because your USD balance ({}) is below your pre-defined threshold ({}). You can update this threshold amount in etc/dcabot.conf, or you can add more funds at https://pro.coinbase.com.

-dcabot
This script is found in {} and run in /etc/cron.daily.
""".format(usd_balance, threshold_daily_buy, sys.argv[0])
        email(email_message)
        exit()




if __name__ == '__main__':
    main()
