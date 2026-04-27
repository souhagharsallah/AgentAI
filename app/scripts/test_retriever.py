from app.rag.retriever import Retriever


def main():
    retriever = Retriever()

    query = "Quels projets faire pour devenir Data Engineer ?"
    results = retriever.retrieve(query, top_k=5, fetch_k=10)

    print(f"\nQuestion : {query}")
    print(f"Nombre de résultats : {len(results)}\n")

    for i, result in enumerate(results, start=1):
        print(f"--- Résultat {i} ---")
        print("Base score :", result["base_score"])
        print("Bonus score :", result["bonus_score"])
        print("Final score :", result["final_score"])
        print("Métadonnées :", result["metadata"])
        print("Texte :", result["text"][:700])
        print()


if __name__ == "__main__":
    main()