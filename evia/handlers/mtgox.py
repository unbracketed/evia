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
        data = json.loads(unicode(message))
        print data
        if data['channel_name'].startswith('ticker') and self.ticker_handler:
            self.ticker_handler(data['ticker'], message)
        elif data['channel_name'].startswith('trade') and self.trade_handler:
            self.trade_handler(data['trade'], message)
        elif data['channel_name'].startswith('depth') and self.depth_handler:
            self.depth_handler(data['depth'], message)

        #TODO lag updates

#https://github.com/ralphtheninja/goxstream
