#! /bin/sh

ps -ef | grep 'performa.py' | grep -v grep | awk '{print $2}' | xargs kill -9
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
python $SCRIPT_DIR/performa.py