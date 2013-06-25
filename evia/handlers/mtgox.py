import json
from ws4py.client.threadedclient import WebSocketClient


class MtGoxWebSocketAPI(WebSocketClient):

    def __init__(self, url, trade_handler=None, ticker_handler=None, depth_handler=None, lag_handler=None):
        super(MtGoxWebSocketAPI, self).__init__(url)
        self.trade_handler = trade_handler
        self.ticker_handler = ticker_handler
        self.depth_handler = depth_handler
        self.lag_handler = lag_handler
        print 'init'

    def opened(self):
        print 'opened'

    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, message):
        #messages may contain unicode currency symbols
        message = json.loads(unicode(message))
        print message
        if message['channel_name'] == 'ticker.BTCUSD' and self.ticker_handler:
            self.ticker_handler(message['ticker'])
        elif message['channel_name'] == 'trade.BTC' and self.trade_handler:
            self.trade_handler(message['trade'])
        elif message['channel_name'] == 'depth.BTCUSD' and self.depth_handler:
            self.depth_handler(message['depth'])

        #TODO lag updates

#https://github.com/ralphtheninja/goxstream
