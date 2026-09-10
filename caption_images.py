import json
import base64
from urllib.request import Request, urlopen
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"

def caption_image(model: str, image_path: str, prompt: str):
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    request = Request(
        OLLAMA_URL,
        data=json.dumps({
            "model": model,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["response"]

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

images = [
    ("multimodal_doc1.txt", "/Users/mikailgondal/Desktop/Screenshot 2026-09-09 at 15.52.28.png"),
    ("multimodal_doc2.txt", "/Users/mikailgondal/Desktop/Screenshot 2026-09-09 at 15.21.19.png"),
]

prompt = "Describe this chart in detail. Include the exact title, every category label, and every exact number or percentage shown."

for filename, image_path in images:
    print(f"Captioning {image_path}...")
    caption = caption_image("llava", image_path, prompt)
    with open(DATA_DIR / filename, "w") as f:
        f.write(caption)
    print(f"Saved {filename}:\n{caption}\n")