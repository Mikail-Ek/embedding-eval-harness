## Results

Full retrieval evaluation run across all six models — 5 questions, cosine similarity between question and document embeddings.

| Model | Size | Dimensions | Category | Correct | Avg Score | Time (s) |
|---|---|---|---|---|---|---|
| all-minilm | 45MB | 384 | Small | 4/5 | 0.543 | 5.9 |
| nomic-embed-text | 274MB | 768 | Small | 5/5 | 0.693 | 6.0 |
| embeddinggemma | 620MB | 768 | Small | 5/5 | 0.556 | 15.8 |
| mxbai-embed-large | 669MB | 1024 | Small | 5/5 | 0.662 | 11.6 |
| nemotron-3-embed-1b | 748MB | 2048 | Small | 5/5 | 0.759 | 28.4 |
| bge-m3 | ~1.2GB | 1024 | Large | 5/5 | 0.648 | 26.3 |
| qwen3-embedding:4b | 2.5GB | 2560 | Large | 5/5 | 0.620 | 94.8 |
| qwen3-embedding:8b | 4.7GB | 4096 | Large | 5/5 | 0.677 | 186.9 |

**Update (follow-up request):** `embeddinggemma` (Google) and `nemotron-3-embed-1b` (NVIDIA, via community GGUF conversion — see [`hf.co/NeoRoth/nemotron-3-embed-1b-gguf`](https://huggingface.co/NeoRoth/nemotron-3-embed-1b-gguf)) were added after the original six-model evaluation. **Nemotron-3-Embed-1B now has the highest average score of any model tested**, beating even qwen3-embedding:8b while running 6.6× faster.

**Key finding:** `nomic-embed-text` (274MB) achieved the highest average confidence score and fastest time among all models that retrieved perfectly, while `qwen3-embedding:8b` (4.7GB) took 14x longer for a comparable result. Accuracy plateaued after the smallest model — additional size and cost bought no further retrieval improvement in this test. This directly supports the presentation's core argument: the highest-benchmark or largest model is not automatically the best production choice.

Full results: `results/results.csv`

## Status

- [x] Docker + Ollama running locally
- [x] Six models pulled and tested across small/large categories
- [x] `embed.py` — reusable embedding function
- [x] Test set (manually authored, 5 questions — automated generation via `generate_testset.py` attempted but too slow on local CPU-only setup)
- [x] Retrieval evaluation (`evaluate.py` — cosine similarity based)
- [x] Results write-up

## Next Steps

- Expand the test set beyond 5 questions for more statistically robust results
- Let `generate_testset.py` run to completion or on stronger hardware for automated, larger-scale test generation