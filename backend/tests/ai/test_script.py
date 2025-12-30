import json
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def get_rag_responses():
    # Charger le dataset
    with open('./backend/tests/ai/questions_1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_value = []
    # Pour chaque question
    for q in data['questions']:
        del q["reponse_attendue"]

        response_ai = client.post("/api/chat", json={
            "prompt": q['question'],
        })
        
        value = response_ai.json().get("response", "")
        if value:
            q["response_ai"] = value

            new_value.append(q)

    # Sauvegarder les réponses dans un nouveau fichier
    with open('./backend/tests/ai/responses_1.json', 'w', encoding='utf-8') as f:
        json.dump(new_value, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_rag_responses()
