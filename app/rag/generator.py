from typing import List, Dict, Any


class AnswerGenerator:
    def build_context(self, results: List[Dict[str, Any]]) -> str:
        parts = []

        for i, result in enumerate(results, start=1):
            metadata = result.get("metadata", {})
            source = metadata.get("file_name", "inconnu")
            formation = metadata.get("formation", "inconnue")
            page = metadata.get("page", "?")
            text = result.get("text", "").strip()

            block = (
                f"[Source {i}]\n"
                f"Formation : {formation}\n"
                f"Fichier : {source}\n"
                f"Page : {page}\n"
                f"Contenu :\n{text}\n"
            )
            parts.append(block)

        return "\n\n".join(parts)

    def generate_answer(self, query: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not results:
            return {
                "question": query,
                "answer": "Désolé, je n'ai trouvé aucune information correspondant à votre recherche dans la base documentaire. N'hésitez pas à reformuler votre question.",
                "sources": [],
                "context": ""
            }

        intro = "Voici les informations que j'ai pu trouver dans la documentation concernant votre question :\n\n"

        answer_parts = []
        sources = []

        for i, result in enumerate(results, start=1):
            metadata = result.get("metadata", {})
            text = result.get("text", "").strip()
            file_name = metadata.get("file_name", "inconnu")
            formation = metadata.get("formation", "inconnue")
            page = metadata.get("page", "?")

            short_text = text[:800]  # On donne un peu plus de texte
            answer_parts.append(
                f"**Extrait {i} (Source : {file_name})** :\n\"{short_text}...\"\n"
            )

            sources.append(
                {
                    "formation": formation,
                    "file_name": file_name,
                    "page": page,
                }
            )

        final_answer = intro + "\n\n".join(answer_parts)
        context = self.build_context(results)

        return {
            "question": query,
            "answer": final_answer,
            "sources": sources,
            "context": context,
        }