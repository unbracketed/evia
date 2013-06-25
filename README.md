# Evia

**Tools for gathering and processing cryptocurrency market data**

## Installation:

**Requires**: Redis

```
virtualenv evia && source $VIRTUAL_ENV/bin/activate
pip install -e git+https://github.com/unbracketed/evia.git#egg=evia
```

Run a Mt. Gox collector that will log ticker, trade, and depth data
to a database and publish to Redis

```
cd $VIRTUAL_ENV/src/evia
python evia/exchanges/mtgox/collector.py
```