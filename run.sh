#!/bin/bash
# copy this script to /etc/cron.daily

BUY_CRYPTO=${1:-eth-usd}
BUY_AMT=${2:-6.00}

set -e
source /home/mike/bin/dcabot/dcabot/bin/activate
/bin/python3 /home/mike/bin/dcabot/dcabot/src/eth-usd.py "$BUY_CRYPTO" "$BUY_AMT" > /home/mike/bin/dcabot/log.txt
deactivate
