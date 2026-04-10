import json
import pandas as pd
from kafka import KafkaConsumer
from pipelines.ultra_advanced_etl import run_full_etl_pipeline
from snowflake_utils.loader import load_to_snowflake
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def run_kafka_batch():

    consumer = KafkaConsumer(
        'market_topic',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode()),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='elite-group'
    )

    buffer = []
    BATCH_SIZE = 50
    TIMEOUT_MS = 5000

    logging.info("🚀 Starting batch consumption...")

    # Controlled polling loop (to prevent infinite loop)
    while len(buffer) < BATCH_SIZE:
        messages = consumer.poll(timeout_ms=TIMEOUT_MS)

        # If no messages, stop trying
        if not messages:
            break

        for tp, msgs in messages.items():
            for msg in msgs:
                buffer.append(msg.value)

                if len(buffer) >= BATCH_SIZE:
                    break

            if len(buffer) >= BATCH_SIZE:
                break

    consumer.close()  #  closing consumer

    if not buffer:
        logging.info(" No data received from Kafka")
        return

    df = pd.DataFrame(buffer)

    # Adding  processing timestamp
    df["processed_time"] = datetime.utcnow()

    logging.info(f"📊 Processing batch of size {len(df)}")

    # Performing ETL transformation
    df_transformed = run_full_etl_pipeline(df)

    # Loading to Snowflake
    load_to_snowflake(df_transformed)

    logging.info(f"Loaded {len(df)} records to Snowflake")
    logging.info("ETL Finished")