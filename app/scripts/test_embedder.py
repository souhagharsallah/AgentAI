import json
from pathlib import Path
from app.rag.embedder import TextEmbedder
def main():
    input_file = Path("app/data/processed/chunks.json")

    if not input_file.exists():
        raise FileNotFoundError(f"Fichier introuvable : {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embedder = TextEmbedder()
    embeddings = embedder.embed_chunks(chunks[:5])

    print("Nombre de chunks testés :", len(chunks[:5]))
    print("Shape embeddings :", embeddings.shape)


if __name__ == "__main__":
    main()