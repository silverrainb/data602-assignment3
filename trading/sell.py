from datetime import date, timedelta, datetime
import gdax_hist as gh
import gdax_display as gd
import pandas as pd


def sell(ledger, gdax):
    """
    Updates current market price. Calculate bid transaction, pass params to exit position in ledger.
    """
    try:
        horizontal_line = "-------------------------"
        tickers = ["BTC-USD", "ETH-USD", "LTC-USD", "BCH-USD"]

        def get_ticker():
            while True:
                choice = int(input(">>>>> Please pick the crypto-pair to trade. \n 1. BTC-USD \n 2. ETH-USD \n 3. "
                                   "LTC-USD \n 4. BCH-USD \n>>"))
                if choice == 1:
                    return tickers[0]
                elif choice == 2:
                    return tickers[1]
                elif choice == 3:
                    return tickers[2]
                elif choice == 4:
                    return tickers[3]

        def hist100():
            """
            displays the last 100 days trade history per day
            """
            hundred = timedelta(100)
            start = date.today() - hundred
            end = date.today()
            return gh.gdax_hist(ticker).fetch(start, end, 1440)

        def hist24():
            """
            displays the last 24 hours trade history per hour
            """
            one = timedelta(1)
            start = date.today() - one
            end = date.today()
            return gh.gdax_hist(ticker).fetch(start, end, 60)

        ticker = get_ticker()
        hist100 = hist100()
        hist100.index = pd.to_datetime(hist100.index, unit='s')

        bid_price = gdax.get(ticker, 'price')

        print(horizontal_line * 2)
        print(ticker, ":", bid_price)
        print(horizontal_line * 2)
        bid_price = float(bid_price)

        while True:
            try:
                bid_quantity = float(input(">>>>> Please type in the quantity you would like to bid: \n>"))
                break
            except ValueError:
                print("Inappropriate format. Please try again.")

        if ledger.get_quantity(ticker) >= bid_quantity:
            bid_transaction = bid_quantity * bid_price
            print("")
            print(">>>>> Basic analytics")

            hist24 = hist24()
            sd24 = hist24['close'].std()
            average24 = hist24['close'].mean()
            min24 = hist24['low'].min()
            max24 = hist24['high'].max()
            print(horizontal_line * 2)
            print("Before confirming the trade, please find the basic analytics as follows:")
            print("Please wait while the graph is loading to display in your default browser.")
            print(horizontal_line * 2)
            gd.gdax_disp(hist100)
            print("To view the display of past 100 days on pop-up. Otherwise click: https://plot.ly/~silverrainb/8")
            print(horizontal_line * 2)
            print("Average price over past 24 hours: {}".format(average24))
            print("Min/Max range over past 24 hours: {}".format(min24, max24))
            print("Standard deviation of price over past 24 hours: {}".format(sd24))
            print(horizontal_line * 2)
            print(">>>>> Would you like to proceed the following transaction?")
            print(horizontal_line * 2)
            print(ticker, ":", bid_price)
            print("Total", " :", "$", bid_transaction)
            print(horizontal_line * 2)
            print("1. Yes. Confirm and proceed the transaction.")
            print("2. No. Cancel the transaction")
            confirm_answer = input(": \n>")

            if confirm_answer == "1":
                side = 'Sell'
                timestamp = datetime.now()
                timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                ledger.exit_position(bid_price, ticker, bid_quantity)
                blotter_cash = ledger.get_current_cash() - bid_transaction
                ledger.update_blotter(side, ticker, bid_quantity, bid_price, timestamp, bid_transaction, blotter_cash)
                ledger.update_pl_cache(timestamp, blotter_cash, bid_transaction)
                print(">>>>> Transaction completed.")
            else:
                print(">>>>> Transaction dismissed.")
        else:
            print(">>>>> Insufficient quantity to sell. Please try again.")
    except ValueError as e:
        print("Selling transaction error.  " + str(e))
