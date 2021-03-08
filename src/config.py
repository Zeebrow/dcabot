import configparser
import sys
import os.path
import dcabot_logging as logall

conf_file = "/home/mike/bin/dcabot/dcabot/etc/dcabot.conf"
secrets_file = "/home/mike/.dcabot_secrets"
#secrets_file = "../etc/dcabot_secrets"

########
# Need to handle errors where files don't exist, etc.
########
def check_files_exist():
    # check conf files and handle errors
    if (not os.path.exists(conf_file)):
        logall("Could not find configuration file at ../etc/dcabot.conf. Exiting! (should ask to generate a new one)")
        exit()
    
    if (not os.path.exists(secrets_file)):
        logall("Could not find secrets file ~/.dcabot_secrets. Exiting!")
        exit()

def get_tracked_currencies():
    tracked_currencies = []
    buy_amt = []
    for section in config.sections():
        if '-usd' in section:
            t = section.upper(),config[section]['daily_buy']
            tracked_currencies.append(t)
    return tracked_currencies

########
# Get all configuration values
# Formatting and typing should be done in this module

# Secrets
secrets = configparser.ConfigParser()
secrets.read(secrets_file)
smtp_username = secrets['email_secrets']['smtp_username']
smtp_password = secrets['email_secrets']['smtp_password']
api_key = secrets['coinbase_secrets']['api_key']
api_secret = secrets['coinbase_secrets']['api_secret']
api_password = secrets['coinbase_secrets']['api_password']

# Configuration
config = configparser.ConfigParser()
config.read(conf_file)
## General
threshold_daily_buy = float(config['general']['threshold_daily_buy'])
dcabot_home = config['general']['home_dir']
secrets_file = config['general']['secrets_file']
## BTC-USD
btcusd_daily_buy = float(config['btc-usd']['daily_buy'])

## ETH-USD
ethusd_daily_buy = float(config['eth-usd']['daily_buy'])

## Email
email_to = config['email']['email_to']
email_from = config['email']['email_from']

## Logging
info_log = config['logging']['info_log']
error_log = config['logging']['error_log']

if __name__ == '__main__':
    print()
    print("________DCAbot_Config________")
    if (len(sys.argv) == 1):
        print("No conf file specified. Reading default (../etc/dcabot.conf).")
        CONF_FILE = conf_file
    else:
        CONF_FILE = sys.argv[1]
        print(f"Reading {CONF_FILE}")
    conf = configparser.ConfigParser()
    conf.read(CONF_FILE)
    print("Sections:")
    print(config.sections())
    print()
    print("General settings:")
    for key in config['general']:
        print("{}: {}".format(key, config['general'][key]))
    print()
    print('btc-usd currency pair settings:')
    for key in config['btc-usd']:
        print("{}: {}".format(key, config['btc-usd'][key]))
    print()
    print('eth-usd currency pair settings:')
    for key in config['eth-usd']:
        print("{}: {}".format(key, config['btc-usd'][key]))
    print()
    print("Email settings:")
    for key in config['email']:
        print("{}: {}".format(key, config['email'][key]))
    print()
    print("Logging settings:")
    for key in config['logging']:
        print("{}: {}".format(key, config['logging'][key]))
