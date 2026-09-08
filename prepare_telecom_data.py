from datasets import load_dataset
from pathlib import Path
import random

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

print("Downloading TeleQnA dataset...")
dataset = load_dataset("SuLLMerica/TeleQnA_Test_With_RAG_Context")
rows = dataset["train"]

random.seed(42)
sample_indices = random.sample(range(len(rows)), 20)  # extra buffer in case some are too short

doc_count = 0
for idx in sample_indices:
    if doc_count >= 12:
        break

    row = rows[idx]
    context_chunks = row["context"]

    cleaned_chunks = []
    for chunk in context_chunks:
        text = chunk
        if "This retrieval is performed from" in text:
            text = text.split("This retrieval is performed from")[0]
        for i in range(1, 6):
            text = text.replace(f"\nRetrieval {i}:\n", " ")
            text = text.replace(f"Retrieval {i}:\n", " ")
        cleaned_chunks.append(text.strip())

    combined_text = " ".join(cleaned_chunks).strip()
    word_count = len(combined_text.split())

    if word_count < 100:
        print(f"Skipping index {idx} — only {word_count} words after cleaning")
        continue

    doc_count += 1
    filename = f"telecom_doc{doc_count}.txt"
    with open(DATA_DIR / filename, "w") as f:
        f.write(combined_text)
    print(f"Saved {filename} ({word_count} words) — from: {row['question'][:60]}...")

print(f"\nDone. Saved {doc_count} telecom documents.")