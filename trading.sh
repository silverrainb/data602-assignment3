#!/usr/bin/env bash

docker network create mongo-network

docker pull mongo:3.7
docker run -d --rm -v `pwd`/db:/data/db --network mongo-network --name trading-database mongo:3.7

#docker pull silverrainb/crypto-forecast
docker build -t crypto-forecast .
#docker run --rm --name trading-app --network mongo-network -it silverrainb/crypto-forecast
docker run --rm --name trading-app --network mongo-network -it crypto-forecast
#docker run --rm --name trading-app --network mongo-network -it crypto-forecast sh -c 'bash'
docker kill trading-database

docker network rm mongo-network
