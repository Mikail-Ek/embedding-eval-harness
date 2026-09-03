## Results

Full retrieval evaluation run across all six models — 5 questions, cosine similarity between question and document embeddings.

| Model | Category | Correct | Avg Score | Time (s) |
|---|---|---|---|---|
| all-minilm | Small | 4/5 | 0.543 | 21.6 |
| nomic-embed-text | Small | 5/5 | 0.693 | 30.3 |
| mxbai-embed-large | Small | 5/5 | 0.662 | 78.8 |
| bge-m3 | Large | 5/5 | 0.648 | 103.4 |
| qwen3-embedding:4b | Large | 5/5 | 0.620 | 221.7 |
| qwen3-embedding:8b | Large | 5/5 | 0.677 | 435.5 |

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