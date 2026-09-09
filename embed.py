import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

OLLAMA_URL = "http://localhost:11434/api/embed"

def get_embedding(model: str, text: str):
    """
    Sends text to a local Ollama model and returns its embedding vector.
    """
    request = Request(
        OLLAMA_URL,
        data=json.dumps({"model": model, "input": text, "keep_alive": 0}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise RuntimeError(f"Ollama request failed with status {error.code}") from error
    return data["embeddings"][0]  # first (and only) embedding returned


if __name__ == "__main__":
    # Quick manual test — same thing your curl commands were doing
    models_to_test = [
    "all-minilm",
    "nomic-embed-text",
    "mxbai-embed-large",
    "bge-m3",
    "qwen3-embedding:4b",
    "qwen3-embedding:8b",
    "embeddinggemma",
    "hf.co/NeoRoth/nemotron-3-embed-1b-gguf:Q4_K_M",
]
    sample_text = "hello world"

    for model in models_to_test:
        vector = get_embedding(model, sample_text)
        print(f"{model}: got a {len(vector)}-dimensional vector")