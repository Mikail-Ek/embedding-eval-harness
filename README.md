# Embedding Evaluation Harness

A local, Ollama-based harness for evaluating embedding models on retrieval accuracy, investigating automated test-set generation with Ragas, and testing multimodal document retrieval — built during VIAVI Solutions work experience (AI/ML).

## Setup

```bash
docker run -d --name ollama -p 11434:11434 -v ollama_storage:/root/.ollama ollama/ollama:latest
docker exec -it ollama ollama pull all-minilm
docker exec -it ollama ollama pull nomic-embed-text
docker exec -it ollama ollama pull mxbai-embed-large
docker exec -it ollama ollama pull bge-m3
docker exec -it ollama ollama pull qwen3-embedding:4b
docker exec -it ollama ollama pull qwen3-embedding:8b
docker exec -it ollama ollama pull embeddinggemma
docker exec -it ollama ollama pull hf.co/NeoRoth/nemotron-3-embed-1b-gguf:Q4_K_M
docker exec -it ollama ollama pull qwen3:8b
docker exec -it ollama ollama pull llava
```

## Repository Structure

| File | Purpose |
|---|---|
| `embed.py` | Reusable embedding function used by all evaluation scripts |
| `evaluate.py` | Six-to-eight-model retrieval evaluation (Part 1) |
| `generate_testset.py` | Ragas automated test-set generation (Part 2) |
| `prepare_squad_data.py`, `prepare_telecom_data.py` | Source document preparation for Ragas generation |
| `caption_images.py` | llava-based image captioning (Part 4, Path A) |
| `evaluate_multimodal.py` | Eight-model retrieval evaluation on captioned images (Part 4, Path A) |
| `test_colpali.py` | ColQwen2 direct image embedding (Part 4, Path B) |
| `data/` | All test sets, source documents, and generated outputs |
| `results/` | Evaluation results (CSV) |

## Part 1 — Embedding Model Evaluation

Eight models evaluated on retrieval accuracy, confidence, and speed, using a fixed five-question test set across three documents.

| Model | Size | Dims | Correct | Avg Score | Time (s) |
|---|---|---|---|---|---|
| all-minilm | 45MB | 384 | 4/5 | 0.543 | 5.9 |
| nomic-embed-text | 274MB | 768 | 5/5 | 0.693 | 6.0 |
| embeddinggemma | 620MB | 768 | 5/5 | 0.556 | 15.8 |
| mxbai-embed-large | 669MB | 1024 | 5/5 | 0.662 | 11.6 |
| **nemotron-3-embed-1b** | 748MB | 2048 | 5/5 | **0.759** | 28.4 |
| bge-m3 | 1.2GB | 1024 | 5/5 | 0.648 | 26.3 |
| qwen3-embedding:4b | 2.5GB | 2560 | 5/5 | 0.620 | 94.8 |
| qwen3-embedding:8b | 4.7GB | 4096 | 5/5 | 0.677 | 186.9 |

**Key finding:** `nemotron-3-embed-1b` (NVIDIA) scored highest overall — beating a model 17x its size (`qwen3-embedding:8b`) while running 6.6x faster. `nomic-embed-text` remains the best efficiency pick among the smaller models.

## Part 2 — Automated Test Generation with Ragas

Investigated why Ragas's synthetic test-generation pipeline was unreliable across several local models.

| Model | Dataset | Docs | Outcome |
|---|---|---|---|
| llama3.2:1b | Original docs | 3 | Never progressed |
| llama3.2:3b | Original docs | 3 | Failed — JSON formatting errors |
| llama3.1:8b | SQuAD (CPU & GPU) | 1–3 | Partial — same failure on both CPU and GPU |
| **qwen3:8b** | SQuAD, Telecom | 3–12 | **Full success on both datasets** |

**Key finding:** reliability depends on whether a model is trained for structured output, not on size or hardware — `qwen3:8b` succeeded consistently where the entire Llama family failed at every size tested, including on GPU. Working generated test sets exist for both a general-domain (SQuAD) and telecom-domain (3GPP/TeleQnA) dataset. A follow-up test also compared `nomic-embed-text` vs. `nemotron-3-embed-1b` as Ragas's internal supporting embedding model — both work, but produce measurably different output character.

## Part 3 — Hardware Requirements & Industry Context

Minimum/recommended CPU and GPU specs documented for all four models used in Part 2. Also includes independent industry research: TeleEmbedBench (validates the Qwen family's strength on telecom-domain content) and GSMA's OTel-Embedding (telecom-specific fine-tuning, +9.6 to +60.2 NDCG@10 points over generic baselines).

## Part 4 — Multimodal Document Retrieval

None of the eight models in Part 1 can process images directly. Two architectures were tested on real chart images:

- **Path A (captioning bridge):** `llava` captions each chart, then the eight report models retrieve against the captions. Result: llava's captions were **0/10 factually correct** on exact numbers, yet retrieval still scored a perfect 6/6 — a real risk, since retrieval success doesn't guarantee correct facts reach the end user.
- **Path B (direct image embedding):** `ColQwen2` embeds the raw image directly,

## Part 5 — Model Licensing & Commercial Use

Full licensing review covering GPL/AGPL exposure, per-model commercial terms, known downsides, and use cases for every model used. None of the models or core libraries are GPL/AGPL. Most are unconditionally commercial-safe (Apache 2.0/MIT); the Llama family, Google's Gemma, and `llava` carry real conditions worth legal review before commercial use. This is research, not legal advice.

## Part 6 — Reranker Models: Baseline Investigation

Baseline (non-tested) research comparing reranker models to the retrieval approaches used throughout this project, per a follow-up request. No rerankers were run — this is architectural and literature-based analysis only.

Key points: every model in Part 1 is a bi-encoder (documents and queries embedded independently, then compared); a reranker is a cross-encoder (query and document processed jointly, no pre-computation possible). Published research shows rerankers lift retrieval accuracy 15–40% on average, at the cost of no pre-computation and poor scaling with candidate count — which is why they're used as a second-stage refinement after embedding-based retrieval, not a replacement for it. Two candidate models identified for future testing: `Qwen3-Reranker` and `BGE-reranker-v2-m3`, both direct siblings of embedding models already tested in Part 1.