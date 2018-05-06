# data602-assignment3


* docker hub link

https://hub.docker.com/r/silverrainb/crypto-forecast/ 

* docker pull

`docker pull silverrainb/crypto-forecast` 

* docker run

`docker run -it silverrrainb/crypto-forecast` 

* docker run with blotter persistency

Please note that for persistency in blotter, pymongo is used. 
Mongodb will reserve data in local specified volume directory. 
Please specify of your path to see the effects in the run commands below.

`docker run -v /Users/username/data602-assignment2/db:/data/db -it silverrainb/crypto-trading`


* Visualization

Plotly has been used for visualization and it is mean to show pop-up screen of the visualization. 
Otherwise, please follow the link console indicates to check.

`https://plot.ly/~silverrainb/10`


* Data source

GDAX websocket is implemented to offer real-time price to trade. As GDAX offers 4 pairs on USDT, the currencies to trade on this demo is: BTC, ETH, LTC and BHC.

For the last 24 hours and 100 days of data to provide insights upon transaction, requests has been used to directly pull daily data using the offered API by GDAX.


* Price forecast

BTC-USD and ETH-USD has price prediction implementing `HOLT-linear`, `ARIMA` model.