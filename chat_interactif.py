from app.main import ask_question, QuestionRequest

print("========================================")
print(" Bienvenue dans le Chatbot RAG Polytech ")
print("========================================")

formation = None
annee = None

while True:
    print("\n----------------------------------------")
    question = input("Vous (Tapez 'quit' pour quitter) : ")
    
    if question.lower() == 'quit':
        break
        
    # On gère l'état de la formation et l'année
    if not formation or not annee:
        req = QuestionRequest(question=question)
        res = ask_question(req)
        print(f"\nChatbot : {res['answer']}")
        
        # Si la question est bloquée par le manque de formation
        if "Avant toute chose" in res['answer']:
            formation_input = input("\n[Système] Entrez votre formation (ex: idu, meca...) : ")
            annee_input = input("[Système] Entrez votre année d'étude (ex: 3, 4, 5) : ")
            
            if formation_input and annee_input:
                formation = formation_input
                annee = annee_input
                print("\n[Système] Merci ! Je cherche la réponse à votre question initiale...")
                
                # On relance la question initiale avec la formation et l'année
                req = QuestionRequest(question=question, formation=formation, annee=annee)
                res = ask_question(req)
                print(f"\nChatbot : {res['answer']}")
                
    else:
        req = QuestionRequest(question=question, formation=formation, annee=annee)
        res = ask_question(req)
        print(f"\nChatbot : {res['answer']}")

print("Au revoir !")
