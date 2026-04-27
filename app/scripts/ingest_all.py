import json
from pathlib import Path

from app.rag.loader import PDFLoader
from app.rag.cleaner import TextCleaner


def main():
    loader = PDFLoader("app/data/raw_pdf")
    cleaner=TextCleaner()

    documents = loader.load_all()
    cleaned_documents = cleaner.clean_documents(documents)

    output_dir = Path("app/data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "cleaned_documents.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_documents, f, ensure_ascii=False, indent=2)
    return documents



if __name__ == "__main__":
    main()