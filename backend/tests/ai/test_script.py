import json
import time
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)


def get_rag_responses():
    with open('./backend/tests/ai/questions_1.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_value = []

    for idx, q in enumerate(data['questions'], start=1):
        del q["reponse_attendue"]

        response_ai = client.post(
            "/api/chat",
            json={"prompt": q['question']}
        )

        value = response_ai.json().get("response", "")
        if value:
            q["response_ai"] = value
            new_value.append(q)

        time.sleep(2)

    with open('./backend/tests/ai/responses_4.json', 'w', encoding='utf-8') as f:
        json.dump(new_value, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_rag_responses()


