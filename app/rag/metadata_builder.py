from typing import List, Dict, Any


class MetadataBuilder:
    def __init__(self):
        pass

    def detect_type_contenu(self, text: str, file_name: str) -> str:
        text_lower = text.lower()
        file_lower = file_name.lower()

        # priorité au nom du fichier (plus fiable)
        if "projet" in file_lower:
            return "projet"
        if "competence" in file_lower:
            return "competence"
        if "metier" in file_lower or "emploi" in file_lower:
            return "metier"
        if "ressource" in file_lower or "experience" in file_lower:
            return "ressource"

        # fallback sur le texte
        if "projet" in text_lower:
            return "projet"
        if "compétence" in text_lower:
            return "competence"
        if "emploi" in text_lower or "stage" in text_lower:
            return "metier"

        return "autre"

    def detect_theme(self, text: str, formation: str) -> str:
        text_lower = text.lower()

        if formation.lower() == "idu":
            if any(word in text_lower for word in ["etl", "pipeline", "kafka", "spark", "airflow"]):
                return "data_engineering"
            if any(word in text_lower for word in ["machine learning", "classification", "régression"]):
                return "data_science"
            return "data"

        if formation.lower() == "batiment":
            return "batiment_construction"

        if formation.lower() == "meca":
            return "mecanique"

        return "general"

    def extract_keywords(self, text: str) -> List[str]:
        keywords_list = [
            "python", "sql", "spark", "kafka", "airflow", "docker",
            "etl", "pipeline", "machine learning", "deep learning",
            "api", "fastapi", "git", "tests", "rgpd"
        ]

        text_lower = text.lower()
        found = []

        for word in keywords_list:
            if word in text_lower:
                found.append(word)

        return found

    def enrich_chunk(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        text = chunk["text"]
        metadata = chunk["metadata"]

        file_name = metadata.get("file_name", "")
        formation = metadata.get("formation", "")

        type_contenu = self.detect_type_contenu(text, file_name)
        theme = self.detect_theme(text, formation)
        keywords = self.extract_keywords(text)

        new_metadata = {
            **metadata,
            "type_contenu": type_contenu,
            "theme": theme,
            "keywords": keywords
        }

        return {
            "text": text,
            "metadata": new_metadata
        }

    def enrich_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        enriched = []

        for chunk in chunks:
            enriched.append(self.enrich_chunk(chunk))

        return enriched