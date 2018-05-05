import threading
from websocket import WebSocketApp
from json import dumps, loads


class gdax_websocket:
    _current = {}
    _ws = {}

    def on_message(self, ws, message):
        msg = loads(message)
        if 'product_id' in msg:
            self._current[msg['product_id']] = msg

    def on_open(self, socket):
        params = {
            "type": "subscribe",
            "channels": [{"name": "ticker", "product_ids": ["BTC-USD", "ETH-USD", "LTC-USD", "BCH-USD"]}]
        }
        socket.send(dumps(params))

    def start(self):
        url = "wss://ws-feed.gdax.com"
        self._ws = WebSocketApp(url, on_open=self.on_open, on_message=self.on_message)
        thread = threading.Thread(target=self._ws.run_forever)
        thread.start()

    def stop(self):
        self._ws.close()

    def get(self, product_id, key):
        return self._current[product_id][key]
