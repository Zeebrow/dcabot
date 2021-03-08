#!/bin/bash

DCABOT_SECRETS=~/.dcabot/secrets

[ $(id -u) != 0 ] && echo "Must be root user to install. Exiting!" && exit 1


