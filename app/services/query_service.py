from app.rag.retriever import Retriever
from app.rag.generator import AnswerGenerator


class QueryService:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = AnswerGenerator()

    def ask(self, question: str, formation: str = None, annee: str = None, top_k: int = 5) -> dict:
        if not formation or not annee:
            return {
                "question": question,
                "answer": "Avant toute chose, pourriez-vous m'indiquer votre formation ainsi que votre année d'étude ?",
                "sources": [],
                "context": ""
            }

        results = self.retriever.retrieve(question, formation=formation, annee=annee, top_k=top_k)
        response = self.generator.generate_answer(question, results)
        return response