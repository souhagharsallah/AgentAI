from typing import List, Dict, Any

from app.rag.embedder import TextEmbedder
from app.rag.vectorstore import FAISSVectorStore


class Retriever:
    def __init__(
        self,
        index_path: str = "app/data/indexes/faiss_index.bin",
        metadata_path: str = "app/data/indexes/faiss_metadata.json",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.embedder = TextEmbedder(model_name=model_name)
        self.store = FAISSVectorStore.load(index_path, metadata_path)

    def _compute_bonus(self, query: str, result: Dict[str, Any], user_formation: str = None, user_annee: str = None) -> float:
        query_lower = query.lower()
        text_lower = result["text"].lower()
        metadata = result.get("metadata", {})
        file_name = metadata.get("file_name", "").lower()
        formation = metadata.get("formation", "").lower()

        bonus = 0.0

        # -----------------------------
        # Bonus liés à la question
        # -----------------------------
        if "projet" in query_lower or "projets" in query_lower:
            if "projet" in text_lower or "projets" in text_lower:
                bonus += 0.15

            if "projets" in file_name:
                bonus += 0.25

        if "data engineer" in query_lower:
            if "data engineer" in text_lower:
                bonus += 0.15

            if any(word in text_lower for word in ["etl", "pipeline", "kafka", "spark", "airflow", "dbt"]):
                bonus += 0.15

            if any(word in file_name for word in ["projets", "competences", "techniques"]):
                bonus += 0.10

        if "data scientist" in query_lower:
            if "data scientist" in text_lower:
                bonus += 0.15

            if any(word in text_lower for word in ["machine learning", "deep learning", "classification", "régression"]):
                bonus += 0.15

        if "compétence" in query_lower or "competence" in query_lower:
            if "compétence" in text_lower or "compétences" in text_lower:
                bonus += 0.15

            if "competences" in file_name:
                bonus += 0.20

        if "outil" in query_lower or "outils" in query_lower:
            if any(word in text_lower for word in ["python", "sql", "docker", "spark", "kafka", "airflow"]):
                bonus += 0.10

        if "stage" in query_lower or "travail" in query_lower or "emploi" in query_lower:
            if any(word in text_lower for word in ["emploi", "stage", "alternance", "recrutent", "marché"]):
                bonus += 0.10

        # -----------------------------
        # Bonus liés au nom du fichier
        # -----------------------------
        if "01_metiers" in file_name or "marche_emploi" in file_name:
            if any(word in query_lower for word in ["emploi", "métier", "metier", "salaire", "marché", "marche"]):
                bonus += 0.20

        if "02_projets" in file_name:
            if any(word in query_lower for word in ["projet", "portfolio", "github", "réaliser", "realiser"]):
                bonus += 0.25

        if "03_competences" in file_name:
            if any(word in query_lower for word in ["compétence", "competence", "outil", "outils", "technique"]):
                bonus += 0.20

        if "04_bonnes_pratiques" in file_name:
            if any(word in query_lower for word in ["bonne pratique", "professionnel", "rgpd", "git", "code propre"]):
                bonus += 0.20

        if "05_experiences" in file_name or "ressources" in file_name:
            if any(word in query_lower for word in ["ressource", "kaggle", "open source", "veille", "expérience", "experience"]):
                bonus += 0.20

        # -----------------------------
        # Pénalisation légère des fichiers trop généraux
        # -----------------------------
        if "onisep" in file_name:
            if "projet" in query_lower or "compétence" in query_lower or "competence" in query_lower:
                bonus -= 0.10

        # -----------------------------
        # Bonus formation si utile
        # -----------------------------
        if formation == "idu":
            if any(word in query_lower for word in ["data", "ml", "ia", "python", "sql", "backend", "api"]):
                bonus += 0.05

        # -----------------------------
        # Bonus formation utilisateur
        # -----------------------------
        if user_formation:
            user_formation_lower = user_formation.lower()
            if formation != "inconnue" and formation != "general":
                if formation == user_formation_lower:
                    bonus += 0.50
                else:
                    # Penalize heavily if the document belongs to another specific formation
                    bonus -= 100.0
            elif formation == "general":
                # Dans un document général, on vérifie si la formation de l'utilisateur est mentionnée
                if user_formation_lower in text_lower:
                    bonus += 1.0
                else:
                    # Si ça parle d'une autre formation et pas de la sienne, on pénalise fortement
                    other_formations = ["idu", "eit", "meca", "batiment", "bee"]
                    if any(f in text_lower for f in other_formations if f != user_formation_lower):
                        bonus -= 100.0

        return bonus

    def _rerank_results(self, query: str, results: List[Dict[str, Any]], user_formation: str = None, user_annee: str = None) -> List[Dict[str, Any]]:
        reranked = []

        for result in results:
            base_score = float(result.get("score", 0.0))
            bonus = self._compute_bonus(query, result, user_formation, user_annee)
            final_score = base_score + bonus

            enriched_result = {
                **result,
                "base_score": base_score,
                "bonus_score": bonus,
                "final_score": final_score,
            }
            reranked.append(enriched_result)

        reranked.sort(key=lambda x: x["final_score"], reverse=True)
        return reranked

    def retrieve(self, query: str, formation: str = None, annee: str = None, top_k: int = 3, fetch_k: int = 30) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.embed_text(query)

        # On récupère plus de résultats que nécessaire
        raw_results = self.store.search(query_embedding, top_k=fetch_k)

        # Puis on rerank
        reranked_results = self._rerank_results(query, raw_results, user_formation=formation, user_annee=annee)

        # On filtre ceux qui ont une pénalité forte
        filtered_results = [r for r in reranked_results if r["final_score"] > -50.0]

        # Enfin on garde les meilleurs
        return filtered_results[:top_k]