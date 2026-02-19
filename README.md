# Schoolassist-ai

AI-powered chatbot designed for small and mid-sized schools to automate parent and student queries.

## Features

- FAQ chatbot using school knowledge base
- PDF ingestion for circulars and policies
- Retrieval-Augmented Generation (RAG)
- FastAPI backend
- Simple Web UI
- Docker-ready deployment

## Use Cases

- Admission queries
- Fee structure explanation
- Homework lookup
- School timing and transport info
- Circular search

## Tech Stack

- FastAPI
- OpenAI API
- FAISS
- Python
- Docker

## Architecture

User → FastAPI → Vector Search (FAISS) → LLM → Response

## Setup

```bash
git clone https://github.com/yourusername/schoolassist-ai.git
cd schoolassist-ai
pip install -r requirements.txt
uvicorn main:app --reload
