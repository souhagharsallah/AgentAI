import re
from typing import List, Dict, Any


class TextCleaner:
    def clean_text(self, text: str) -> str:
        if not text:
            return ""

        text = text.strip()
        text = text.replace("\t", " ")

        # Nettoyer les espaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Supprimer les espaces autour des retours ligne
        text = re.sub(r" *\n *", "\n", text)

        # Fusionner les lignes cassées simples
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        merged_lines = []

        for line in lines:
            if not merged_lines:
                merged_lines.append(line)
                continue

            prev = merged_lines[-1]

            # Si la ligne précédente ne se termine pas par ponctuation
            # et que la nouvelle ligne n'est pas une puce, on fusionne
            if (
                not prev.endswith((".", ":", ";", "?", "!"))
                and not line.startswith(("•", "-", "*"))
                and len(prev) < 120
            ):
                merged_lines[-1] = prev + " " + line
            else:
                merged_lines.append(line)

        text = "\n".join(merged_lines)

        # Réduire les gros blocs de sauts de ligne
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def clean_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "text": self.clean_text(document["text"]),
            "metadata": document["metadata"],
        }

    def clean_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned_documents = []

        for doc in documents:
            cleaned_doc = self.clean_document(doc)
            if cleaned_doc["text"]:
                cleaned_documents.append(cleaned_doc)

        return cleaned_documents