
WITH base AS (
 SELECT * FROM market_data
),
w1 AS (
 SELECT symbol,timestamp,close,volume,
 AVG(close) OVER (PARTITION BY symbol ORDER BY timestamp ROWS BETWEEN 10 PRECEDING AND CURRENT ROW) AS ma10,
 STDDEV(close) OVER (PARTITION BY symbol ORDER BY timestamp ROWS BETWEEN 10 PRECEDING AND CURRENT ROW) AS vol
 FROM base
),
w2 AS (
 SELECT *,
 LAG(close) OVER (PARTITION BY symbol ORDER BY timestamp) AS prev_close
 FROM w1
),
final AS (
 SELECT *,
 (close-prev_close)/prev_close AS returns,
 CASE WHEN vol>2 THEN 1 ELSE 0 END AS anomaly_flag
 FROM w2
)
SELECT * FROM final;
