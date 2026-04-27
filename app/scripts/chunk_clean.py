import json
from pathlib import Path

from app.rag.chunker import TextChunker


def main():
    input_file = Path("app/data/processed/cleaned_documents.json")
    output_file = Path("app/data/processed/chunks.json")

    if not input_file.exists():
        raise FileNotFoundError(f"Fichier introuvable : {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        cleaned_documents = json.load(f)

    chunker = TextChunker(chunk_size=800, overlap=150)
    chunks = chunker.chunk_documents(cleaned_documents)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()