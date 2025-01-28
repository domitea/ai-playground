FROM python:3.11-bookworm

#RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

RUN pip install --progress-bar off fastapi uvicorn redis sentence-transformers chromadb \
    opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi \
    opentelemetry-exporter-otlp

WORKDIR /app
COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]