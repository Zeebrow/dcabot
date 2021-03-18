from dca_config import config
import os.path
import logging

#
# Set of methods to handle some basic tasks outside of main.py
#

########
# Need to handle errors where files don't exist, etc.
########

logger = logging.getLogger(__name__)


def check_files_exist(config_file=config.DEFAULT_CONFIG_FILEPATH):
    # check conf files and handle errors
    if (not os.path.exists(config_file)):
        logger.error(f"Could not find configuration file {config_file}. Exiting!") # (should ask to generate a new one
        return False
    return True

def get_tracked_currencies():
    tracked_currencies = []
    buy_amt = []
    for section in config.config.sections():
        if '-usd' in section:
            t = section.upper(),config[section]['daily_buy']
            tracked_currencies.append(t)
    return tracked_currencies

def generate_new_configfile():
    pass

def validate_config(config_file):
    # Check for vars, catch typos (You want to buy HOW MUCH?!)
    pass

def default_trigger(daily_buy_total: float, current_balance: float):
    logger.warn("Unable to get low balance alert level from configuration!")
    logger.warn(f"Defaulting to 2x daily buy total (${2*daily_buy_total:.2f})")
    if 2*daily_buy_total > current_balance:
        return True
    else:
        return False

def trigger_low_bal_alert(low_bal_level: str, current_balance: float, daily_buy_total: float):
    try:
        low_bal_level = float(low_bal_level)
        if low_bal_level < current_balance:
            return True
        else:
            return False
    except ValueError:
        try:
            multiplier = int(low_bal_level[:-1])
            if multiplier*daily_buy_total > current_balance:
                return True
            else:
                return False
        except ValueError:
            return default_trigger(daily_buy_total, current_balance)
    else:
        return default_trigger(daily_buy_total, current_balance)

