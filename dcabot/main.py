#!/usr/bin/python3
import cbpro, json, requests, sys
import os.path
import sys
from time import sleep
from datetime import datetime
from dca_config import config as conf
from dca_config import config_utils
from notifications.send_email import email
from dca_config import SecretsManager as SM
from constants import *
import logging

# main.py
# k.i.s.s. (LOL)
###
# These need to be moved out into their own module!
#

global _is_test

if 'test' in sys.argv:
    _is_test = True
    log_format = logging.Formatter( '--TEST--%(asctime)s - %(name)s - %(levelname)s - %(message)s' )# TODO set in constants.py
else:
    _is_test = False
    log_format = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )# TODO set in constants.py

logger = logging.getLogger()

def place_buy(auth_client, currency, amount):
    currency = currency.upper()
    amount = float(amount)
    order_details = auth_client.place_market_order(product_id=currency,
            side='buy',
            funds=amount)
    if "id" in order_details:
        logger.info(f"Order placed for ${amount:.2f} of {currency}.")
        sleep(0.05)
        receipt = confirm_order(auth_client, order_details['id'])
        if ('message' in receipt):
            logger.error(f"{receipt['message']}")
        else:
            logger.debug(f"{currency} order details:\n" + json.dumps(order_details, indent=2))
            return order_details
    else:

        logger.debug(f"Order for ${amount:.2f} of {currency} was never placed (You have not been charged).")
        logger.debug(f"message:\n>{order_details['message']}")
        return False

def confirm_order(auth_client, order_id):
    o = auth_client.get_order(order_id)
    if 'message' in o:
        logger.error(f"There was a problem confirming order {order_id}")
        logger.error(f"Message:\n{o['message']}")
        return False
    logger.info(f"Confirmed order {o['product_id']} for ${float(o['funds']):.2f} (Fee: ${float(o['fill_fees']):.4f}).")
    return o


def test():

    logger.setLevel(logging.DEBUG)  
    logfile_path = 'dcabot.log' # TODO set in constants.py
    fh = logging.FileHandler(logfile_path)
    sh = logging.StreamHandler()
    sh.setFormatter(log_format)
    fh.setFormatter(log_format)
    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.info(" in test() - Testing DCABot")
    if(not config_utils.check_files_exist()):
        raise FileNotFoundError("Configuration file not found.")
    
    tracked_currencies = conf.get_tracked_currencies()
    threshold_daily_buy = 42069.1337
    btcusd_daily_buy = 0.0
    ethusd_daily_buy = 0.0
    bchusd_daily_buy = 0.0
    total_sought_usd = btcusd_daily_buy + ethusd_daily_buy + bchusd_daily_buy
    
    auth_client = SM.SecretsManager().cbpro_auth_client()
    all_accounts = auth_client.get_accounts()
    
    usd_balance = 0.0
    for acct in all_accounts:
        if (acct['currency'] == "USD"):
            usd_balance = float(acct['balance'])
            logger.debug("Ignoring actual account balance for testing.")
            logger.info(f"Ignoring actual account balance for testing: ${usd_balance:.2f}")
    usd_balance = 696969.420
    logger.info(f"Avalable balance to trade: ${usd_balance:.2f}")
    if (usd_balance > threshold_daily_buy):
        if (usd_balance < total_sought_usd):
            logger.error(f"Insufficient funds to buy! \nUSD balance:\t${usd_balance}\nTotal sought:\t${total_sought_usd:.2f}")
            # TODO:
            # email(fail_msg)
            exit(1)
        for curr_amt_pair in tracked_currencies:
            this_buy = place_buy(auth_client, curr_amt_pair[0], curr_amt_pair[1])
            sleep(0.05) # I dunno y
            if ( this_buy ):
                _confirm = confirm_order(auth_client, this_buy['id'])
                if (not _confirm):
                    logger.error("Oh shit. Your order was placed successfully, but we can't confirm that it went through.")
                else:
                    logger.info(f"Successfully bought ${curr_amt_pair[1]} of {curr_amt_pair[0]}")

    else:
        logger.error(f"Insufficient funds! (balance: ${usd_balance:.2f}, threshold balance: ${threshold_daily_buy:.2f})")
        exit(1)
def main():

    logger.setLevel(logging.INFO)  
    logfile_path = 'dcabot.log' # TODO set in constants.py
    fh = logging.FileHandler(logfile_path)
    sh = logging.StreamHandler()
    sh.setFormatter(log_format)
    fh.setFormatter(log_format)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.info("Starting DCABot")

    if _is_test:
        threshold_daily_buy = 999999.0

    if(not config_utils.check_files_exist()):
        raise FileNotFoundError("Configuration file not found.")
    
    tracked_currencies = conf.get_tracked_currencies()
    threshold_daily_buy = conf.threshold_daily_buy
    btcusd_daily_buy = conf.btcusd_daily_buy
    ethusd_daily_buy = conf.ethusd_daily_buy
    bchusd_daily_buy = conf.bchusd_daily_buy
    total_sought_usd = btcusd_daily_buy + ethusd_daily_buy + bchusd_daily_buy
    
    auth_client = SM.SecretsManager().cbpro_auth_client()
    all_accounts = auth_client.get_accounts()
    
    usd_balance = 0.0
    for acct in all_accounts:
        if (acct['currency'] == "USD"):
            usd_balance = float(acct['balance'])
    logger.info(f"Avalable balance to trade: ${usd_balance:.2f}")
    if (usd_balance > threshold_daily_buy):
        if (usd_balance < total_sought_usd):
            logger.error(f"Insufficient funds to buy! \nUSD balance:\t${usd_balance}\nTotal sought:\t${total_sought_usd:.2f}")
            # TODO:
            # email(fail_msg)
            exit(1)
        for curr_amt_pair in tracked_currencies:
            this_buy = place_buy(auth_client, curr_amt_pair[0], curr_amt_pair[1])
            sleep(0.05) # I dunno y
            if ( this_buy ):
                _confirm = confirm_order(auth_client, this_buy['id'])
                if (not _confirm):
                    logger.error("Oh shit. Your order was placed successfully, but we can't confirm that it went through.")
                else:
                    logger.info(f"Successfully bought ${curr_amt_pair[1]} of {curr_amt_pair[0]}")

    else:
        logger.error(f"Insufficient funds! (balance: ${usd_balance:.2f}, threshold balance: ${threshold_daily_buy:.2f})")
        email_message = """
Sup,
Your daily trade was not executed because your USD balance ({}) is below your pre-defined threshold ({}). You can update this threshold amount in etc/dcabot.conf, or you can add more funds at https://pro.coinbase.com.

-dcabot
This script is found in {} and run in /etc/cron.daily.
""".format(usd_balance, threshold_daily_buy, sys.argv[0])
        
        if (not _is_test):
            email(email_message)

        exit(1)

if __name__ == '__main__':
    if 'test' in sys.argv:
        test()
    else:
        main()
