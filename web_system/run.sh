#!/bin/bash
DIR="$( cd "$( dirname "$0" )" && pwd )"
echo $DIR

cd $DIR

# ulimit -n 50000
nohup gunicorn --config=bysms/gunicorn_conf.py bysms.wsgi &> /dev/null &

VERSION = '1.5'