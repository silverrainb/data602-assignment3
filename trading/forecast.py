import numpy as np
import pandas as pd
from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.api import Holt


def timetodate(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')


def datetotime(date):
    return datetime.strptime(date, '%Y-%m-%d').timestamp()


def fetchcrypto(ticker):
    # function fetches a crypto price-series to store in dataframe

    cols = ['date', 'timestamp', 'open', 'high', 'low', 'close']
    lst = ['time', 'open', 'high', 'low', 'close']

    timetoday = datetime.today().timestamp()
    current_time = timetoday

    for j in range(2):
        df = pd.DataFrame(columns=cols)
        limit = 900
        url = "https://min-api.cryptocompare.com/data/histoday?fsym=" + ticker + "&tsym=USD" + "&toTs=" + str(
            int(current_time)) + "&limit=" + str(limit)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dic = json.loads(soup.prettify())
        for i in range(1, limit):
            tmp = []
            for e in enumerate(lst):
                x = e[0]
                y = dic['Data'][i][e[1]]
                if x == 0:
                    tmp.append(str(timetodate(y)))
                tmp.append(y)
            if np.sum(tmp[-4::]) > 0:
                df.loc[len(df)] = np.array(tmp)
        df.index = pd.to_datetime(df.date)
        df.drop('date', axis=1, inplace=True)
        current_time = int(df.iloc[0][0])
        if j == 0:
            df_copy = df.copy()
        else:
            data = pd.concat([df, df_copy], axis=0)
            data = data[['timestamp', 'close']]
            data['close'] = data['close'].astype(float)
    return data


def get_crypto_data(tickers):

    data = pd.DataFrame()

    for ticker in tickers:
        ticker = ticker
        crypto_data = fetchcrypto(ticker)
        data = pd.concat([data, crypto_data['close']], axis=1)
        data = data.dropna(axis=0, how='any')

    data.columns = tickers
    return data


def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return np.array(diff)


def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]


def forecast_arima(ticker, data):
    ticker = str(ticker).upper()
    dataset = data[ticker]

    X = dataset.values
    year = 365
    diff = difference(X, year)

    model = ARIMA(diff, order=(7, 0, 1))
    model_fit = model.fit(disp=0)

    start_index = len(diff)
    end_index = len(diff)
    fc_arima = model_fit.predict(start=start_index, end=end_index)
    fc_arima = inverse_difference(X, fc_arima, year)
    return fc_arima[0]


def forecast_holt(ticker, data):
    ticker = str(ticker).upper()
    dataset = data[ticker]

    X = dataset.values
    year = 365
    diff = difference(X, year)

    model = Holt(diff).fit(smoothing_level = 0.3,smoothing_slope = 0.1)
    fc_holt = model.forecast()
    fc_holt = inverse_difference(X, fc_holt, year)
    return fc_holt[0]
