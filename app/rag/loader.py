from pathlib import Path
from typing import List, Dict, Any
import fitz


class PDFLoader:
    def __init__(self, raw_data_dir: str = "app/data/raw_pdf"):
        self.raw_data_dir = Path(raw_data_dir)

    def load_pdf(self, pdf_path: Path, formation: str) -> List[Dict[str, Any]]:
        documents = []
        try:
            pdf = fitz.open(pdf_path)
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text")
                cleaned_text = "\n".join(
                    line.strip() for line in text.splitlines() if line.strip()
                )

                documents.append(
                    {
                        "text": cleaned_text,
                        "metadata": {
                            "source": str(pdf_path),
                            "file_name": pdf_path.name,
                            "formation": formation,
                            "page": page_number,
                        },
                    }
                )

            pdf.close()

        except Exception as e:
            print(f"[ERREUR] Impossible de lire {pdf_path}: {e}")

        return documents

    def load_formation(self, formation: str) -> List[Dict[str, Any]]:
        formation_path = self.raw_data_dir / formation

        if not formation_path.exists():
            #print(f"[ATTENTION] Dossier introuvable : {formation_path}")
            return []

        all_documents = []

        for pdf_path in formation_path.glob("*.pdf"):
            #print(f"[INFO] Lecture du PDF : {pdf_path}")
            docs = self.load_pdf(pdf_path, formation)
            all_documents.extend(docs)

        return all_documents

    def load_all(self) -> List[Dict[str, Any]]:
        all_documents = []

        if not self.raw_data_dir.exists():
            #print(f"[ERREUR] Le dossier {self.raw_data_dir} n'existe pas.")
            return []

        for formation_dir in self.raw_data_dir.iterdir():
            if formation_dir.is_dir():
                formation = formation_dir.name
                #print(f"[INFO] Chargement de la formation : {formation}")
                docs = self.load_formation(formation)
                all_documents.extend(docs)

        return all_documents