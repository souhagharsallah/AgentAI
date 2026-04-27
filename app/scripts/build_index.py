import json
from pathlib import Path

from app.rag.embedder import TextEmbedder
from app.rag.vectorstore import FAISSVectorStore


def main():
    input_file = Path("app/data/processed/enriched_chunks.json")
    index_file = Path("app/data/indexes/faiss_index.bin")
    metadata_file = Path("app/data/indexes/faiss_metadata.json")

    if not input_file.exists():
        raise FileNotFoundError(f"Fichier introuvable : {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embedder = TextEmbedder()
    embeddings = embedder.embed_chunks(chunks)

    dimension = embeddings.shape[1]
    store = FAISSVectorStore(dimension=dimension)
    store.add_embeddings(embeddings, chunks)
    store.save(index_file, metadata_file)


if __name__ == "__main__":
    main()