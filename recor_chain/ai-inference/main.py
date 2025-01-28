from fastapi import FastAPI
import redis
import chromadb
import hashlib
from sentence_transformers import SentenceTransformer
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

app = FastAPI()

# Připojení k Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# Připojení k ChromaDB s HNSW indexem
vector_db = chromadb.HttpClient(host="chromadb", port=8000)
collection = vector_db.get_or_create_collection(name="chat_history", metadata={"hnsw:space": "cosine"})

# OpenTelemetry setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer_provider().get_tracer("ai-inference")
span_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(span_exporter))

# Model pro embeddingy
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


@app.get("/predict")
def predict(query: str):
    with tracer.start_as_current_span("SLM Service: predict") as span:
        span.add_event(f"Processing query: {query}")

        # Hashování dotazu pro Redis
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        cached_response = redis_client.get(query_hash)

        if cached_response:
            span.add_event("Cache hit")
            return {"response": cached_response, "cached": True}

        # Převod dotazu na embedding
        query_embedding = model.encode(query).tolist()

        # Hledání v ChromaDB
        results = collection.query(query_embeddings=[query_embedding], n_results=3)

        if results["metadatas"] and results["metadatas"][0]:
            best_matches = [meta["text"] for meta in results["metadatas"][0] if "text" in meta]
            span.add_event("Vektorová DB nalezla odpověď")
            return {"response": best_matches, "cached": False}

        # Eskalace na LLM pokud je dotaz delší než 10 slov
        if len(query.split()) > 10:
            span.add_event("Eskalace na LLM")
            return {"response": "LLM_REQUIRED"}

        # Generování odpovědi pomocí SLM
        response = f"SLM odpověď: {query}"

        # Uložení do Redis s TTL
        redis_client.setex(query_hash, 86400, response)

        # Uložení embeddingu do ChromaDB
        collection.add(
            ids=[query_hash],
            embeddings=[query_embedding],
            metadatas=[{"text": response}]
        )

        span.end()

        return {"response": response, "cached": False}