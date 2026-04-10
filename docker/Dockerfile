
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install pandas numpy kafka-python psycopg2 fastapi uvicorn yfinance torch tensorflow
EXPOSE 8000
CMD ["uvicorn","api.app:app","--host","0.0.0.0","--port","8000"]
