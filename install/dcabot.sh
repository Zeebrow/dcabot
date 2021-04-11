#!/bin/bash
# copy this script to /etc/cron.daily

#LOG_FILE=/home/mike/bin/dcabot/log.txt
LOG_FILE=/home/mike/bin/dcabot/dcabot/logs/cron.log

set -e
source /home/mike/bin/dcabot/dcabot/bin/activate
echo $(date) >> $LOG_FILE
/bin/python3 /home/mike/bin/dcabot/dcabot/src/main.py cron >> $LOG_FILE
echo "Done." >> $LOG_FILE
echo "------------------------------------------------------" >> $LOG_FILE
deactivate
