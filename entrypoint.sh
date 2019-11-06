#!/bin/sh

# set -e

cron

echo "Cron is running!" >> /var/log/tilebuilder.log

tail -n 25 -f /var/log/tilebuilder.log
