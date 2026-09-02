# Embedding Model Evaluation Harness

Prototype evaluation harness for testing the production viability of open-source embedding models for RAG, built during work experience at VIAVI Solutions.

## Purpose

This repo does two things:
1. Categorizes open-source embedding models into **small** (runs comfortably on Mac) and **large** (heavier resource requirements) buckets
2. Prototypes an evaluation harness to compare retrieval quality and latency across models, using Ragas-generated test questions

## Setup

Models run locally via [Ollama](https://ollama.com), inside Docker for consistency.

1. Start the Ollama container:
```bash
docker run -d --name ollama -p 11434:11434 -v ollama_storage:/root/.ollama ollama/ollama:latest
```

2. Pull a model:
```bash
docker exec -it ollama ollama pull <model-name>
```

3. Confirm it returns an embedding:
```bash
curl http://localhost:11434/api/embed -d '{"model": "<model-name>", "input": "hello world"}'
```

> **Note:** Docker on Mac cannot access Apple Silicon's GPU — all models here run CPU-only inside the container. Latency numbers reflect CPU-only performance, not native Mac GPU performance.

## Models Tested

| Model | Size | Dimensions | Category | Notes |
|---|---|---|---|---|
| `all-minilm` | 45MB | 384 | Small | Near-instant response |
| `nomic-embed-text` | 274MB | 768 | Small | |
| `mxbai-embed-large` | 669MB | 1024 | Small | |
| `bge-m3` | ~1.2GB | 1024 | Large | |
| `qwen3-embedding:4b` | 2.5GB | 2560 | Large | Same model family as the 8B version, for a direct size comparison |
| `qwen3-embedding:8b` | 4.7GB | 4096 | Large | ~57s server load time on first request, ~7.4GB RAM used |

All six models pulled via Ollama and confirmed working via `/api/embed`.

## Project Structure

```
embedding-eval-harness/
├── README.md          # this file
├── embed.py            # reusable function to call Ollama's /api/embed
├── data/                # source documents for test generation (not yet populated)
└── results/             # evaluation output (not yet populated)
```

## Status

- [x] Docker + Ollama running locally
- [x] Six models pulled and tested across small/large categories
- [x] `embed.py` — reusable embedding function
- [ ] Ragas test set generation
- [ ] Retrieval evaluation (Context Precision / Context Recall)
- [ ] Results write-up

## Next Steps

1. Install Ragas, generate a synthetic test set from sample documents
2. Build `evaluate.py` — run retrieval across all six models, score with Context Precision/Recall
3. Save results to `results/`