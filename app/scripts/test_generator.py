from app.rag.retriever import Retriever
from app.rag.generator import AnswerGenerator


def main():
    retriever = Retriever()
    generator = AnswerGenerator()

    query = "Quels projets faire pour devenir Data Engineer ?"
    results = retriever.retrieve(query, top_k=5)

    response = generator.generate_answer(query, results)

    print("\n===== QUESTION =====\n")
    print(response["question"])

    print("\n===== REPONSE =====\n")
    print(response["answer"])

    print("\n===== SOURCES =====\n")
    for source in response["sources"]:
        print(source)


if __name__ == "__main__":
    main()