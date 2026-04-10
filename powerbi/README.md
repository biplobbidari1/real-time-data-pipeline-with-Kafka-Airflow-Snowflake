Power BI Setup:
1. Connect to PostgreSQL or Snowflake
2. Import table: market_data
3. Create Measures:
   Avg Price = AVERAGE(close)
   Total Volume = SUM(volume)
   Volatility = STDEV(close)
   Anomaly Count = COUNTROWS(FILTER(market_data, anomaly_flag=1))
4. Dashboards:
   - Price trend (line chart)
   - Volume (bar chart)
   - Volatility heatmap
   - Anomaly scatter plot
   - RSI & MACD visualization
   - Gold vs Forex comparison
   - Intraday trend
   - Moving averages
   - Risk score KPI
   - Fraud probability KPI
   - Time-based drilldown
   - Sector comparison
   - Correlation matrix
   - Rolling volatility charts
   - Alert dashboard
   - Streaming dashboard
   - Real-time insights
   - Portfolio analytics
   - Trend detection
   - Outlier tracking