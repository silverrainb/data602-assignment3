#!/usr/bin/env bash

cd /usr/src/app/trading
git pull
mongod > mongo.log &
python3 /usr/src/app/trading/trading/main.py