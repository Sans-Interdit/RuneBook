from qdrant_client import QdrantClient
from data.models import Guide, SessionLocal
import os
from dotenv import load_dotenv
from mistralai import Mistral
import requests

load_dotenv(".env.development")

mistral = Mistral(api_key=os.getenv("LLM_KEY"))


client = QdrantClient(
    url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_KEY"), timeout=5.0
)

API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
headers = {"Authorization": f"Bearer {os.getenv('HF_KEY')}"}


def embed(text):
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    response.raise_for_status()
    return response.json()


def insert_chunk(payload: dict):
    response = mistral.chat.complete(
        model="ministral-8b-latest",
        messages=[
            {
                "role": "system",
                "content": f"""Tu es un système d’indexation sémantique.
À partir du texte fourni, produis un texte destiné exclusivement à un modèle d’embedding.

Contraintes :
- longueur cible : 300 à 450 caractères
- inclure tous les concepts fonctionnels importants
- phrases factuelles, explicites et génériques
- aucun style narratif
- aucune opinion
- aucun pronom ambigu
- aucun exemple pédagogique
- vocabulaire League of Legends conservé
- pas de mise en forme, pas de listes

Puis contenir explicitement, dans le texte, les informations suivantes :
- concept principal
- contexte d’utilisation
- conditions ou limitations
- objectif fonctionnel

Le titre est : {payload['title']}
Les tags sont : {payload['tags']}
Le guide est pour les : {payload['level']}

Texte source :
{payload['content']}""",
            }
        ],
        temperature=0,
    )

    indexed_text = response.choices[0].message.content

    vector = embed(indexed_text)

    client.upsert(
        collection_name="lol_guides",
        points=[{"id": payload["id_guide"], "vector": vector, "payload": payload}],
    )


if __name__ == "__main__":
    db_session = SessionLocal()

    try:
        all_guides = db_session.query(Guide).all()

        all_ids = [guide.id_guide for guide in all_guides]

        existing_result = client.retrieve(
            collection_name="lol_guides",
            ids=all_ids,
            with_payload=True,
            with_vectors=False,
        )

        existing_ids = {point.id for point in existing_result}

        guides_to_insert = [g for g in all_guides if g.id_guide not in existing_ids]

        print(f"{len(guides_to_insert)} guides to insert into Qdrant.")

        for guide in guides_to_insert:
            insert_chunk(guide.to_dict_full())

    finally:
        db_session.close()
