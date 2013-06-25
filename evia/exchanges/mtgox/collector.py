import time
from datetime import datetime

from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from evia.exchanges.mtgox import db
from evia.handlers.mtgox import MtGoxWebSocketAPI

DATABASE = 'sqlite:///mtgox-market-data.db'


def convert_mtgox_timestamp(ts):
    return datetime.fromtimestamp(float(ts)*0.000001)


class Collector:

    def init_db(self):
        print 'init db'
        engine = create_engine(DATABASE, echo=True)
        db.Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        self.db_session = Session()

    def handle_trade(self, data, raw_data):
        trade = db.MtGoxTrade(
            type=data['type'],
            date=datetime.fromtimestamp(data['date']),
            amount=data['amount'],
            price=data['price'],
            tid=data['tid'],
            price_currency=data['price_currency'],
            trade_type=data['trade_type'],
            primary=data['primary'],
            properties=data['properties'])
        self.db_session.add(trade)
        self.db_session.commit()
        self.redis_client.publish('trades.mtgox', raw_data)

    def handle_ticker(self, data, raw_data):
        market_state = db.MtGoxTicker(
            timestamp=convert_mtgox_timestamp(data['now']),
            #FIXME needs to be timezone aware
            time_received=datetime.utcnow(),
            symbol=data['high']['currency'],
            high=data['high']['value'],
            low=data['low']['value'],
            avg=data['avg']['value'],
            vwap=data['vwap']['value'],
            vol=data['vol']['value'],
            last_local=data['last_local']['value'],
            last_orig=data['last_orig']['value'],
            last_all=data['last_all']['value'],
            last=data['last']['value'],
            buy=data['buy']['value'],
            sell=data['sell']['value'])
        self.db_session.add(market_state)
        self.db_session.commit()
        self.redis_client.publish('ticker.mtgox', raw_data)

    def handle_depth(self, data, raw_data):
        depth = db.MtGoxDepth(
            type=data['type'],
            type_str=data['type_str'],
            price=data['price'],
            volume=data['volume'],
            currency=data['currency'],
            timestamp=convert_mtgox_timestamp(data['now']))
        self.db_session.add(depth)
        self.db_session.commit()
        self.redis_client.publish('depth.mtgox', raw_data)

    def run(self):
        self.init_db()
        self.redis_client = Redis()
        self.handler = MtGoxWebSocketAPI(
            'ws://websocket.mtgox.com/mtgox?Currency=USD',
            trade_handler=self.handle_trade,
            ticker_handler=self.handle_ticker,
            depth_handler=self.handle_depth
        )
        print dir(self.handler)
        print 'attempting connect'
        self.handler.connect()


if __name__ == '__main__':
    try:
        collector = Collector()
        collector.run()
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print 'Attempting to close websocket'
        collector.handler.close()
    except Exception, e:
        print e
        print 'Attempting to close websocket'
        collector.handler.close()
