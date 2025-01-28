from fastapi import FastAPI, WebSocket
import requests
import asyncio
import redis
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

app = FastAPI()
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# OpenTelemetry setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer_provider().get_tracer("api-gateway")
span_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(span_exporter))

SLM_URL = "http://ai-inference:8001/predict?query="
LLM_URL = "http://llm-inference:9002/llm?query="

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        span = tracer.start_span("API Gateway Request")
        span.add_event(f"Received query: {data}")

        cached_response = redis_client.get(data)
        if cached_response:
            await websocket.send_json({"response": cached_response, "cached": True})
            span.end()
            continue

        slm_response = requests.get(SLM_URL + data).json()
        if slm_response["response"] != "LLM_REQUIRED":
            redis_client.set(data, slm_response["response"])
            await websocket.send_json({"response": slm_response["response"], "cached": False})
            span.end()
            continue

        await websocket.send_json({"response": "Přesměrováno na LLM..."})
        llm_response = requests.get(LLM_URL + data).json()
        redis_client.set(data, llm_response["response"])

        await websocket.send_json({"response": llm_response["response"], "cached": False})
        span.end()