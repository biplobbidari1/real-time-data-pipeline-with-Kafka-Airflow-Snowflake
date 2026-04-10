import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd

load_dotenv()

def load_to_snowflake(df):

    #  converting timestamps BEFORE insert
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if "processed_time" in df.columns:
        df["processed_time"] = pd.to_datetime(df["processed_time"], errors="coerce")

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO STREAM_DATA (
                symbol, timestamp, close, volume,
                returns, volatility, rsi, macd,
                anomaly_flag, processed_time
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row.get("symbol"),

            # converting to Python datetime (for snowflake support)
            row["timestamp"].to_pydatetime() if pd.notnull(row["timestamp"]) else None,

            float(row.get("close", 0)),
            float(row.get("volume", 0)),
            float(row.get("returns", 0)),
            float(row.get("volatility", 0)),
            float(row.get("rsi", 0)),
            float(row.get("macd", 0)),
            int(row.get("anomaly_flag", 0)),

            # same for processed_time
            row["processed_time"].to_pydatetime() if pd.notnull(row["processed_time"]) else None
        ))

    conn.commit()
    cur.close()
    conn.close()