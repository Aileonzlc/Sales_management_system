#!/bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
echo $DIR

cd $DIR

# ulimit -n 50000
nohup gunicorn web_system.wsgi:application --config=web_system/gunicorn_conf.py &> /dev/null &