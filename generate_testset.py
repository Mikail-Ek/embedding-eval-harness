from importlib import import_module
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

# Load these lazily so environments using an external LangChain installation
# do not fail static import resolution before the script starts.
_document_loaders = import_module("langchain_community.document_loaders")
DirectoryLoader = _document_loaders.DirectoryLoader
TextLoader = _document_loaders.TextLoader
_ollama = import_module("langchain_ollama")
ChatOllama = _ollama.ChatOllama
OllamaEmbeddings = _ollama.OllamaEmbeddings
_ragas_llms = import_module("ragas.llms")
LangchainLLMWrapper = _ragas_llms.LangchainLLMWrapper
_ragas_embeddings = import_module("ragas.embeddings")
LangchainEmbeddingsWrapper = _ragas_embeddings.LangchainEmbeddingsWrapper
_ragas_testset = import_module("ragas.testset")
TestsetGenerator = _ragas_testset.TestsetGenerator

# Load all doc files from data
loader = DirectoryLoader(str(DATA_DIR), glob="doc1.txt", loader_cls=TextLoader)
docs = loader.load()
print(f"Loaded {len(docs)} documents")

# Local models Ragas will use to generate questions
generator_llm = LangchainLLMWrapper(ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434"))
generator_embeddings = LangchainEmbeddingsWrapper(OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434"))

generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)

# Generate a small test set (5 questions)
dataset = generator.generate_with_langchain_docs(docs, testset_size=5)

# Save so evaluate.py can reuse it later without regenerating
dataset.to_pandas().to_json(str(DATA_DIR / "testset.json"), orient="records", indent=2)
print("Saved test set to data/testset.json")