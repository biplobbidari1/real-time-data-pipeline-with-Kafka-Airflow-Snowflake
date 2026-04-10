import yfinance as yf
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode(),
    linger_ms=20,
    batch_size=65536
)

TICKERS = ["AAPL", "MSFT", "GC=F", "EURUSD=X"]

def fetch():
    df = yf.download(" ".join(TICKERS), period="1d", interval="1m", group_by="ticker")

    for t in TICKERS:
        try:
            tdf = df[t].dropna()
            for i, r in tdf.iterrows():
                producer.send("market_topic", {
                    "symbol": t,
                    "timestamp": str(i),
                    "close": float(r["Close"]),
                    "volume": float(r["Volume"])
                })
        except Exception as e:
            print(e)

while True:
    fetch()
    producer.flush()
    time.sleep(60)