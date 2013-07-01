import threading

import redis


CRYPTO_CURRENCIES = [u'BTC', u'LTC']
FIAT_CURRENCIES = [u'AUD', u'BRL', u'CAD', u'CHF', u'CNY', u'DKK', u'EUR', u'GBP',
    u'HKD', u'JPY', u'NZD', u'PLN', u'RUB', u'SEK', u'SGD', u'SLL', u'THB', u'USD']


class TickerEventThread(threading.Thread):
    name = 'Evia-Ticker-Event-Sink'


class MarketState:

    def __init__(self):

        self.redis_client = redis.Redis()

        # Initialize market data structures

        self.periods = ('1m', '3m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1d', '3d', '1w')

        self.tickers = {
            'BTC': {},
            'LTC': {},
        }
        for cc in CRYPTO_CURRENCIES:
            self.tickers[cc] = \
                dict([(
                    fiat_currency,
                    dict([(
                        interval,
                        dict(high=0., low=0., open=0., close=0.))
                        for interval in self.periods]))
                    for fiat_currency in FIAT_CURRENCIES])

    def start_interval_timer(self):
        self.interval_timer = threading.Timer(60, self.handle_timer)
        self.interval_timer.name = 'Evia-Interval-Timer'
        self.interval_timer.start()

    def start(self):
        # Start threads
        self.start_interval_timer()

        #start a thread to receive pubsub messages
        self.ticker_updates_thread = TickerEventThread(target=self.listen_on_ticker_updates)
        self.ticker_updates_thread.start()

    def stop(self):
        print "shutting down"
        self.interval_timer.cancel()
        self.redis_client.publish('ticker.mtgox', 'STOP')

    def handle_timer(self):
        """Closes the 1-minute interval and any others that need it"""
        #close 1m
        #check others
        print "1 minute timer"

        #restart timer
        self.start_interval_timer()

    def listen_on_ticker_updates(self):
        print 'TE thread starting'
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe('ticker.mtgox')
        event_stream = pubsub.listen()
        while True:
            print "listening"
            message = event_stream.next()
            print message
            if message['data'] == 'STOP':
                break
        print 'exiting ticker listener'

    def handle_ticker_update(self, data):
        #update current candles

        high = data['high']
        low = data['low']

        goxticker = self.tickers['mtgox']
        for period in goxticker:

            goxticker[period]['value'] = data['value']

            if high > goxticker[period]['high']:
                #publish mtgox-ticker-<period>-high
                goxticker[period]['high'] = high

            if low < goxticker[period]['low']:
                #publish mtgox-ticker-<period>-low
                goxticker[period]['low'] = low


if __name__ == '__main__':
    import time
    try:
        m = MarketState()
        m.start()
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        m.stop()
