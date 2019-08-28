
# Cryptocurrency Trading Platform

Keywords: Python, Docker, AWS, EC2, MongoDB, API, Visualization, Analytics, Plotly, Time Series Forecast, Predictive Model, Linear Regression, ARIMA, HOLT

This application is a console-based (shell or terminal-based)  cryptocurrency trading demo built-in Python, using real-time data via GDAX api. The application takes orders to buy or sell, a list of predefined currencies and maintain a blotter and P/L.

This Github repo contains Python code for a crypto-trading project, Dockerfile and README file containing a link to Docker image in Docker Hub. Starting the app using Docker doest not require any additional setup steps beyond the installation of Docker, pulling and running of image.

* How to start the program

`./trading.sh`

This shell script initiates mongo, pulling the docker image and running it.

* Docker Hub link

https://hub.docker.com/r/silverrainb/project-crypto-forecast/

* Visualization

Plotly has been used for visualization and it is meant to show a pop-up screen of the visualization. Otherwise, please follow a link shown in the console.

* Price forecast

BTC-USD and ETH-USD has price prediction implementing `HOLT-linear`, `ARIMA` model.

When the program starts, the following menus show:

1. Trade
2. Show Blotter
3. Show P/L
4. Show P/L Records
5. Show P/L Chart
6. Quit

After executing a menu option the user is always brought back to the main menu.

* Trade

If the user wishes to make a trade they will select Trade from the main menu. The user will then be given the list of cryptocurrency pairs, available to trade via GDAX API. The user is allowed to pick a pair and state a quantity, then asked to confirm the trade at the market ask price.

After a trader picks the pair to trade and on the entry screen where s/he will enter quantity, display a chart showing the price of the last 100 days.

If the trade is a buy then the dollar amount of the trade will be deducted from the cash position, if funds are available. Otherwise, the trade is not allowed.

If the trade is a sell then the quantity sold will be deducted from the current equity position held, if any.

`Ask` price of the market is pulled just before executing the trade. Prices change fast and there can be a delay between when you display the market price to the user and when they choose to confirm the trade. The delay is the user’s problem.

* Show Blotter

Blotter displays the trade blotter, a list of historic trades made by the user. It is persisted into a MongoDB and cached using data structures. 

1. Timestamp
2. Side
3. ticker
4. Volume
5. PricePerShare
6. totalCosts
7. Cash

* Show P/L

P/L displays the profit/loss statement. The P/L data will be stored using pandas DataFrames. ARIMA and HOLT is a price prediction column, forecasted using the last 2 years of data.

1. Ticker 
2. Position 
3. Current Market Price 
4. VWAP 
5. UPL (Unrealized P/L) 
6. RPL (Realized P/L)
7. Total P/L
8. Allocation By Shares: the percentage of shares for this stock over total shares in the whole portfolio
9. Allocation By Dollars: which is the percentage of dollars
10. ARIMA: price prediction
11. HOLT: price prediction

Chart of the following in time series is available:

1. Cash position in the P/L
2. Total portfolio P/L
3. VWAP for any crypto in the P/L
4. Executed price history for any crypto

* Basic Analytics

For each crypto that is about to trade, some analytics is produced for that specific crypto and display before the trader confirms the trade, namely:

1. Average price over past 24 hours
2. Min and Max range over the past 24 hours
3. Standard deviation of prices over past 24 hours

* Visualizations

After the trader selects the stock s/he wishes to trade, the following displays show using plotly:

1. The 100-day trade history chart.
2. The 20-day moving average

* Portfolio Size

The initial size of the portfolio is $100MM of cash with no equity positions.

