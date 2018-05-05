import pandas as pd
from pymongo import MongoClient
import record as dr

mongo_client = MongoClient('trading-database', 27017)
db = mongo_client['crypto']


def initialize_pl():
    """
    initialize position
    """
    columns = ['Ticker', 'Position', 'Market', 'WAP', 'UPL', 'RPL', 'Total P/L', 'ShareAllocation %',
               'CashAllocation %', 'ARIMA', 'HOLT']
    ticker_index = pd.Series(["BTC-USD", "ETH-USD", "LTC-USD", "BCH-USD"])
    positions = pd.DataFrame(columns=columns, index=ticker_index)
    positions = positions.fillna(0)
    return positions


class Ledger:
    """
    Ledger manages both blotter and p/l. Blotter stores transaction history and P/L(position) summarizes current balance
    """
    _cash = 0
    _WAP = 0
    _UPL = 0
    _RPL = 0

    blotter_columns = ('Buy|Sell', 'Ticker', 'Volume', 'PricePerShare', 'Timestamp', 'TotalCosts', 'Cash')
    pl_cache_columns = ('Timestamp', 'Cash', 'Total_PL', 'VWAP', 'ExecutedPrice')

    def __init__(self, initial_cash):
        self._blotter = pd.DataFrame([], columns=self.blotter_columns).set_index("Timestamp")
        self._pl_cache = pd.DataFrame([], columns=self.pl_cache_columns).set_index("Timestamp")
        self._cash = initial_cash
        self._positions = initialize_pl()

    def get_current_cash(self):
        """
        Cash is initialized in main for 100MM and updates whenever transaction occurs.
        """
        return self._cash

    def add_position(self, price_per_share, ticker, volume):
        """
        Calculates Position, WAP, UPL when Buy transaction occurs.
        """

        self._cash = self._cash - price_per_share * volume

        current_volume = float(self._positions.loc[ticker, ['Position']])
        updated_volume = float(current_volume + volume)

        current_wap = float(self._positions.loc[ticker, ['WAP']])
        updated_wap = ((current_volume * current_wap) + (volume * price_per_share)) / updated_volume

        self._positions.loc[ticker, ['WAP']] = updated_wap
        self._positions.loc[ticker, ['Position']] = updated_volume

        upl = updated_volume * (float(self._positions.loc[ticker, ['Market']]) - updated_wap)
        self._positions.loc[ticker, ['UPL']] = upl

    def exit_position(self, price_per_share, ticker,
                      volume):
        """
        Calculates Position, WAP, RPL when Sell transaction occurs.
        """
        self._cash = self._cash + price_per_share * volume

        current_volume = float(self._positions.loc[ticker, ['Position']])
        updated_volume = current_volume - volume

        prev_wap = float(self._positions.loc[ticker, ['WAP']])

        current_rpl = float(self._positions.loc[ticker, ['RPL']])
        updated_rpl = current_rpl + (
                volume * (price_per_share - prev_wap))
        self._positions.loc[ticker, ['RPL']] = updated_rpl

        def sold_wap():
            if updated_volume == 0:
                updated_wap = 0
                return updated_wap
            else:
                updated_wap = float(self._positions.loc[ticker, ['WAP']])
                return updated_wap

        wap = sold_wap()
        self._positions.loc[ticker, ['WAP']] = wap

        upl = updated_volume * (
                float(self._positions.loc[ticker, ['Market']]) - wap)
        self._positions.loc[ticker, ['Position']] = updated_volume
        self._positions.loc[ticker, ['UPL']] = upl

    def update_positions(self, gdax):
        """
        Updates real time price information in P/L and summarize current status.
        """
        try:
            btcusd = gdax.get('BTC-USD', 'price')
            ethusd = gdax.get('ETH-USD', 'price')
            ltcusd = gdax.get('LTC-USD', 'price')
            bchusd = gdax.get('BCH-USD', 'price')

            price_values = pd.Series([float(btcusd), float(ethusd), float(ltcusd), float(bchusd)])
            self._positions['Market'] = price_values.values
            self._positions['UPL'] = self._positions['Position'] * (self._positions['Market'] - self._positions['WAP'])
            self._positions['Total P/L'] = self._positions['UPL'] + self._positions['RPL']
            self._positions['ShareAllocation %'] = round(
                (self._positions['Position'] / self._positions['Position'].sum()) * 100, 2)
            self._positions['CashAllocation %'] = round((self._positions['Position'] * self._positions['Market'] / (
                    self._positions['Position'] * self._positions['Market']).sum()) * 100, 2)

            tickers = ['BTC', 'ETH', 'LTC']
            data = dr.get_crypto_data(tickers)
            btc_pred = dr.forecast('BTC', data)
            eth_pred = dr.forecast('ETH', data)
            self._positions.loc['BTC-USD', ['ARIMA']] = btc_pred
            self._positions.loc['ETH-USD', ['ARIMA']] = eth_pred
            btc_pred_b = dr.linear('BTC', data)
            eth_pred_b = dr.linear('ETH', data)
            self._positions.loc['BTC-USD', ['HOLT']] = btc_pred_b
            self._positions.loc['ETH-USD', ['HOLT']] = eth_pred_b
            print(self._positions)
            print('CASH    ', self._cash)

        except ValueError as e:
            print("The P/L is unavailable at the moment." + str(e))

    def get_quantity(self, ticker):
        position = self._positions['Position'][ticker]
        position = float(position)
        return position

    def update_blotter(self, side, ticker, quantity, price, timestamp, transaction, cash):
        """
        The parameters for update_blotter function grabs all information when the
        transaction occurs in both buy.py and sell.py and updates the blotter accordingly.
        """
        self._blotter = self._blotter.append(
            dict(zip(self.blotter_columns, (side, ticker, quantity, price, timestamp, transaction, cash))),
            ignore_index=True).sort_values(by='Timestamp', ascending=False)

        records = {'Side': side,
                   'Ticker': ticker,
                   'Volume': quantity,
                   'PricePerShare': price,
                   'Timestamp': timestamp,
                   'TotalCosts': transaction,
                   'Cash': cash}

        db.blotter_collection.insert(records)

    def print_blotter(self):
        # print blotter from mongodb
        data = pd.DataFrame(list(db.blotter_collection.find()))
        data = data[['Timestamp', 'Side', 'Ticker', 'Volume', 'PricePerShare', 'TotalCosts', 'Cash']].sort_values(by='Timestamp', ascending=False)
        print(data)

    def update_pl_cache(self, timestamp, blotter_cash, executed_price):
        # cash, total_pl, vwap from self._positions
        # when trade confirms, update_pl_cache acts.

        self._pl_cache = self._pl_cache.append(
            dict(zip(self.blotter_columns, ('Timestamp', 'Cash', 'Total P/L', 'VWAP', 'ExecutedPrice'))),
            ignore_index=True).sort_values(by='Timestamp', ascending=False)

        cache = {'Timestamp': timestamp,
                 'Cash': blotter_cash,
                 'Total_PL': self._positions['Total P/L'].astype(float).sum(),
                 'VWAP': self._positions['WAP'].astype(float).sum(),
                 'ExecutedPrice': executed_price}

        db.positions_collection.insert(cache)

    def print_pl_cache(self):
        pl_data = pd.DataFrame(list(db.positions_collection.find()))
        pl_data = pl_data[['Timestamp', 'Cash', 'Total_PL', 'VWAP', 'ExecutedPrice']].sort_values(
            by='Timestamp', ascending=False)
        return pl_data