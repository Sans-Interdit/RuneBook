from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PayloadSchemaType
)
import os
import dotenv

dotenv.load_dotenv(".env.development")


COLLECTION_NAME = "lol_champions"
VECTOR_SIZE = 384

print(os.getenv("QDRANT_URL"))
print(os.getenv("QDRANT_KEY"))
def create_collection():
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_KEY"),
        timeout=5.0
    )

    # Suppression optionnelle (décommentez si nécessaire)
    # client.delete_collection(COLLECTION_NAME)

    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in collections:
        print(f"Collection '{COLLECTION_NAME}' already exists.")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )

    # Définition explicite du schéma de payload
    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="champion",
        field_schema=PayloadSchemaType.KEYWORD
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="chunk_type",
        field_schema=PayloadSchemaType.KEYWORD
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="spell_slot",
        field_schema=PayloadSchemaType.KEYWORD
    )

    print(f"Collection '{COLLECTION_NAME}' created successfully.")

if __name__ == "__main__":
    create_collection()
