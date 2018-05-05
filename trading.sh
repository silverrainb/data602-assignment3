#!/usr/bin/env bash

docker pull mongo:3.7
docker run -d --rm -v /Users/rosekoh/OneDrive/DATA602/assignment3/data602-assignment3/db:/data/db --name trading-database mongo:3.7
#docker run -d --rm -v /Users/username/data602-assignment3/db:/data/db --name trading-database mongo:3.7
#docker pull silverrainb/crypto-forecast
docker build -t crypto-forecast .
#docker run --rm --name trading-app --link trading-database:mongo -v /Users/username/data602-assignment3/db:/data/db -it silverrainb/crypto-forecast
docker run --rm --name trading-app --link trading-database:mongo -it crypto-forecast
docker kill trading-database

