import torch
from PIL import Image
from colpali_engine.models import ColQwen2, ColQwen2Processor

# Use Apple Silicon GPU (MPS) if available, otherwise fall back to CPU
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

model_name = "vidore/colqwen2-v1.0"

print("Loading model (downloads several GB on first run — be patient)...")
model = ColQwen2.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16 if device != "cpu" else torch.float32,
).to(device).eval()

processor = ColQwen2Processor.from_pretrained(model_name)

# Point this at any image with a table/chart in it — e.g. one of today's screenshots
image = Image.open("/path/to/your/screenshot.png")

image_inputs = processor.process_images([image]).to(device)
with torch.no_grad():
    image_embedding = model(**image_inputs)
print(f"Image embedded — shape: {image_embedding.shape}")

query = "What does this table show?"
query_inputs = processor.process_queries([query]).to(device)
with torch.no_grad():
    query_embedding = model(**query_inputs)

score = processor.score_multi_vector(query_embedding, image_embedding)
print(f"Similarity score: {score}") 