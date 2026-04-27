from app.services.query_service import QueryService


def main():
    service = QueryService()

    question = "Quels projets faire pour devenir Data Engineer ?"
    response = service.ask(question, top_k=5)

    print("\n===== QUESTION =====\n")
    print(response["question"])

    print("\n===== REPONSE =====\n")
    print(response["answer"])

    print("\n===== SOURCES =====\n")
    for source in response["sources"]:
        print(source)


if __name__ == "__main__":
    main()