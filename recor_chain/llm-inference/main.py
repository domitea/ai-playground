from fastapi import FastAPI
import openai
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

app = FastAPI()

# OpenTelemetry setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer_provider().get_tracer("llm-inference")
span_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(span_exporter))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.get("/llm")
def llm_inference(query: str):
    with tracer.start_as_current_span("LLM Inference Request") as span:
        span.add_event(f"Processing LLM query: {query}")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Jsi AI expert, odpověz co nejlépe."},
                      {"role": "user", "content": query}]
        )

        span.add_event("LLM odpověď dokončena")
        return {"response": response["choices"][0]["message"]["content"]}