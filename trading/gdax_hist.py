from datetime import timedelta
from time import sleep
import pandas as pd
import requests


class gdax_hist:
    def __init__(self, pair):
        self.pair = pair
        self.uri = 'https://api.gdax.com/products/{pair}/candles'.format(pair=self.pair)

    def fetch(self, start, end, granularity):
        data = []
        delta = timedelta(minutes=granularity * 100)

        slice_start = start
        while slice_start != end:
            slice_end = min(slice_start + delta, end)
            data += self.request_slice(slice_start, slice_end, granularity)
            slice_start = slice_end

        data_frame = pd.DataFrame(data=data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        data_frame.set_index('time', inplace=True)
        return data_frame

    def request_slice(self, start, end, granularity):
        retries = 3
        for retry_count in range(0, retries):
            response = requests.get(self.uri,
                                    {'start': gdax_hist.__date_to_iso8601(start),
                                     'end': gdax_hist.__date_to_iso8601(end),
                                     'granularity': granularity * 60})
            if response.status_code != 200 or not len(response.json()):
                if retry_count + 1 == retries:
                    raise Exception('Failed to get exchange data for ({}, {})!'.format(start, end))
                else:
                    sleep(1.5 ** retry_count)
            else:
                result = sorted(response.json(), key=lambda x: x[0])
                return result

    @staticmethod
    def __date_to_iso8601(date):
        return '{year}-{month:02d}-{day:02d}'.format(year=date.year, month=date.month, day=date.day)
