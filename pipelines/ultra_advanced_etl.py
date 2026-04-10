
import pandas as pd
import numpy as np
import hashlib
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

WINDOWS = [5,10,20,50]

def enforce_schema(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    return df

def clean(df):
    df = df[(df["close"]>0)&(df["volume"]>0)]
    df = df[df["close"] < df["close"].quantile(0.999)]
    return df

def dedup(df):
    df["hash"] = df.apply(lambda r: hashlib.sha256(
        f"{r['symbol']}_{r['timestamp']}_{r['close']}".encode()).hexdigest(), axis=1)
    return df.drop_duplicates("hash")

def sort(df):
    return df.sort_values(["symbol","timestamp"])

def returns(df):
    df["returns"] = df.groupby("symbol")["close"].pct_change()
    df["log_returns"] = np.log(df["close"]/df["close"].shift(1))
    return df

def rolling(df):
    for w in WINDOWS:
        df[f"ma_{w}"] = df.groupby("symbol")["close"].rolling(w).mean().reset_index(0,drop=True)
        df[f"std_{w}"] = df.groupby("symbol")["close"].rolling(w).std().reset_index(0,drop=True)
    return df

def volatility(df):
    df["volatility"] = df["std_20"] * np.sqrt(252)
    return df

def rsi(df):
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain/(loss+1e-9)
    df["rsi"] = 100 - (100/(1+rs))
    return df

def macd(df):
    ema12 = df["close"].ewm(span=12).mean()
    ema26 = df["close"].ewm(span=26).mean()
    df["macd"] = ema12 - ema26
    return df

def anomaly(df):
    df["zscore"] = (df["close"]-df["ma_20"])/(df["std_20"]+1e-9)
    df["anomaly_flag"] = (abs(df["zscore"])>3).astype(int)
    return df

def volume(df):
    df["vol_spike"] = df["volume"]/(df["volume"].rolling(10).mean()+1e-9)
    df["volume_anomaly"] = (df["vol_spike"]>3).astype(int)
    return df

def normalize(df):
    for c in ["close","volume","returns","volatility"]:
        df[c+"_norm"] = (df[c]-df[c].mean())/(df[c].std()+1e-9)
    return df

def partition(df):
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["day"] = df["timestamp"].dt.day
    return df

def metadata(df):
    df["processed_time"] = datetime.utcnow()
    df["batch_id"] = f"batch_{int(datetime.utcnow().timestamp())}"
    return df

def run_full_etl_pipeline(df):
    logging.info("START ETL")
    df = enforce_schema(df)
    df = clean(df)
    df = dedup(df)
    df = sort(df)
    df = returns(df)
    df = rolling(df)
    df = volatility(df)
    df = rsi(df)
    df = macd(df)
    df = anomaly(df)
    df = volume(df)
    df = normalize(df)
    df = partition(df)
    df = metadata(df)
    logging.info("END ETL")
    return df.fillna(0)
