import cbpro, json, requests, sys
from datetime import datetime
from send_email import email

THRESHOLD_DAILY_BUY = 5000.00
BUY_CRYPTO = sys.argv[1].upper()
BUY_AMT = float(sys.argv[2])
dollars = 0.0

email_message = """
Sup,
You tried to buy ${:.2f} of the currency pair {}, but you only have ${:.2f} available to trade.
Since this is above your set threshold of ${:.2f}, your trade was not executed.
Login to Coinbase and add more funds at https://pro.coinbase.com

-dcabot
This script is found in {} and run in /etc/cron.daily.
""".format(BUY_AMT, BUY_CRYPTO, dollars, THRESHOLD_DAILY_BUY, sys.argv[0])
# DCA profile, dcabot keyname
SECRET_B64 = 'd3p3VWp1ZG6WtRslLoIbggJxl7QNJQzjm4XvrQ9n9rziXrG6ZjBiCzkGD07O3nYXpqrXOCHVDzOq/vDW9X2m2g=='
API_KEY = '3b5ac500a3545f9515439cc242fbcdb1'
KEY_PASS = 'wkwjycgzm8'

# coinbase pro creds - dcabot
SECRET_B64 = 'ogj2vpuH4B3YQ484G1mmTQbY8TSJxeB4F0oHyEzPI87dr/fHrbtZ4vYhy3x8mLcB9EpUyGmlT6ZZEMxGfmggOg=='
API_KEY = '450b812a405b5b0437d92a0a037856a4'
KEY_PASS = '6b3lvw2f4qo'

# coinbase take2
#SECRET_B64 = 'AFH1IP6TVWqFOWNc8oDYLzQyXw5yRUiVKSabgFtzPM7RDBlg3aZW1iwJLKyfWU1NnstcnJ4giN/RR3EVrXRw5g==' 
#API_KEY = 'f21d0b0fd3c8742b4c00cf4951f74c5f'
#KEY_PASS = '00p5cfdypfom'


print("--------------------------------------------------------")
print(datetime.now().isoformat())
print("eth-usd.py")
print("Found in /home/mike/bin/dcabot/dcabot/src/eth-usd/py")

auth_client = cbpro.AuthenticatedClient(
        key=API_KEY,
        b64secret=SECRET_B64,
        passphrase=KEY_PASS)


# pretty print contents
# print(json.dumps(auth_client.get_accounts(), indent=2))

accts = auth_client.get_accounts()
for acct in accts:
    if (acct['currency'] == 'USD'):
        dollars = float(acct['balance'])
#    if ( float(acct['balance']) > 0):
#        print(json.dumps(acct, indent=2))

print(f'Avalable balance to trade: {dollars:.2f}')

# buy $5.00 of ETH if USD account balance is above a threshold
if (dollars > THRESHOLD_DAILY_BUY):
    auth_client.place_market_order(product_id=BUY_CRYPTO,
                               side='buy',
                               funds=BUY_AMT)
    print(f"Bought ${BUY_AMT:.2f} of {BUY_CRYPTO}!")
else:
    print(f"Insufficient funds! (balance: ${dollars:.2f}, threshold balance: ${THRESHOLD_DAILY_BUY:.2f})")
    email(email_message)
    exit()

print(f"Fee rate: { auth_client._send_message( method='get', endpoint='/fees', params=None, data=None )['maker_fee_rate'] }")
print()
