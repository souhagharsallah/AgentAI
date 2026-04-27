import json
from pathlib import Path

from app.rag.metadata_builder import MetadataBuilder


def main():
    input_file = Path("app/data/processed/chunks.json")
    output_file = Path("app/data/processed/enriched_chunks.json")

    if not input_file.exists():
        raise FileNotFoundError(f"Fichier introuvable : {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    builder = MetadataBuilder()
    enriched_chunks = builder.enrich_chunks(chunks)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enriched_chunks, f, ensure_ascii=False, indent=2)

    print("DONE")


if __name__ == "__main__":
    main()