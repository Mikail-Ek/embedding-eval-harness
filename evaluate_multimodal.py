import math
import json
import time
from pathlib import Path
from embed import get_embedding

def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))
    return dot_product / (magnitude_a * magnitude_b)

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"

MODELS = [
    "all-minilm",
    "nomic-embed-text",
    "mxbai-embed-large",
    "bge-m3",
    "qwen3-embedding:4b",
    "qwen3-embedding:8b",
    "embeddinggemma",
    "hf.co/NeoRoth/nemotron-3-embed-1b-gguf:Q4_K_M",
]

DOCUMENTS = ["multimodal_doc1.txt", "multimodal_doc2.txt"]

with open(DATA_DIR / "multimodal_testset.json") as f:
    testset = json.load(f)

doc_texts = {}
for doc_name in DOCUMENTS:
    with open(DATA_DIR / doc_name) as f:
        doc_texts[doc_name] = f.read()

print(f"Loaded {len(testset)} questions and {len(doc_texts)} documents")

results = []

for model in MODELS:
    print(f"\n--- Testing {model} ---")
    start_time = time.time()

    doc_vectors = {}
    for doc_name, doc_text in doc_texts.items():
        doc_vectors[doc_name] = get_embedding(model, doc_text)

    correct_count = 0
    all_scores = []

    for item in testset:
        question = item["question"]
        expected = item["expected_source"]
        question_vector = get_embedding(model, question)

        best_doc = None
        best_score = -1
        for doc_name, doc_vector in doc_vectors.items():
            score = cosine_similarity(question_vector, doc_vector)
            if score > best_score:
                best_score = score
                best_doc = doc_name

        is_correct = (best_doc == expected)
        all_scores.append(best_score)
        if is_correct:
            correct_count += 1

        print(f"  Q: {question[:50]}...")
        print(f"     Retrieved: {best_doc} (score: {best_score:.3f}) | Expected: {expected} | {'✓' if is_correct else '✗'}")

    average_score = sum(all_scores) / len(all_scores)
    elapsed_time = time.time() - start_time
    results.append({
        "model": model,
        "correct": correct_count,
        "total": len(testset),
        "avg_score": average_score,
        "time_seconds": elapsed_time,
    })

print("\n=== FINAL RESULTS ===")
for r in results:
    print(f"{r['model']}: {r['correct']}/{r['total']} correct (avg score: {r['avg_score']:.3f}, time: {r['time_seconds']:.1f}s)")