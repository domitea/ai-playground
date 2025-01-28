# 🚀 AI Orchestration System with Docker Compose

This project sets up an AI orchestration system using **Docker Compose**. It includes components for **API gateway, AI inference, LLM inference, Redis, ChromaDB, OpenTelemetry (OTEL) tracing, and Jaeger for observability**.

## 🎯 Motivation

The goal of this project is to **explore the limitations of modern Large Language Models (LLMs)** by building an **AI orchestration system** that allows for **experimentation, benchmarking, and observability**. 

### **Why?**
Despite the impressive capabilities of LLMs, they still struggle with:
- **Hallucinations** (confidently generating false information)
- **Context retention** (losing track of long conversations)
- **Reasoning and logical consistency** (especially in multi-step problems)
- **Efficiency in resource-constrained environments** (edge computing & embedded AI)

By designing an **end-to-end AI pipeline**, we aim to **analyze, debug, and test these issues in real-world scenarios**.

---

## 📌 Project Overview

| Service         | Description | Working somnehow? |
|----------------|-------------|------- |
| **API Gateway** (`api-gateway`) | Central entry point for AI orchestration, handling requests and dispatching them to inference engines. |  ✅ |
| **AI Inference** (`ai-inference`) | Service responsible for AI model inference. The local one... | Not yet |
| **LLM Inference** (`llm-inference`) | Large Language Model inference backend. | ✅ OpenAI, HG pending |
| **Redis** (`redis`) | Caching and data store for fast lookups. | ✅ |
| **ChromaDB** (`chromadb`) | Vector database for storing embeddings and similarity search. | ✅ |
| **Frontend** (`frontend`) | Web interface for interacting with the AI system. | ✅ |
| **OpenTelemetry Collector** (`otel-collector`) | Observability pipeline to collect and send tracing data. | ✅ |
| **Jaeger** (`jaeger`) | Distributed tracing UI for analyzing system performance. | ✅ |

---
