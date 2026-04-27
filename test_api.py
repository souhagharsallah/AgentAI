import json
from app.main import ask_question, QuestionRequest

try:
    print("--- TEST 1 : Question sans formation ni année ---")
    req1 = QuestionRequest(question="Quels sont les débouchés après cette formation ?")
    res1 = ask_question(req1)
    print(json.dumps(res1, indent=2, ensure_ascii=False))

    print("\n--- TEST 2 : Question avec formation et année ---")
    req2 = QuestionRequest(
        question="Quels sont les débouchés après cette formation ?",
        formation="idu",
        annee="4"
    )
    res2 = ask_question(req2)
    print(json.dumps(res2, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"Erreur lors du test: {e}")
