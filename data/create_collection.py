from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PayloadSchemaType
)

COLLECTION_NAME = "lol_champions"
VECTOR_SIZE = 768

def create_collection():
    client = QdrantClient(
        url="http://localhost:6333"
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
        field_name="metadata.positions",
        field_schema=PayloadSchemaType.KEYWORD
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="metadata.classes",
        field_schema=PayloadSchemaType.KEYWORD
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="metadata.legacy",
        field_schema=PayloadSchemaType.KEYWORD
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="metadata.resource",
        field_schema=PayloadSchemaType.KEYWORD
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="metadata.range_type",
        field_schema=PayloadSchemaType.KEYWORD
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="metadata.adaptive_type",
        field_schema=PayloadSchemaType.KEYWORD
    )

    # Stats (filtrables numériquement)
    for stat in ["damage", "toughness", "control", "mobility", "utility"]:
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=f"stats.{stat}",
            field_schema=PayloadSchemaType.INTEGER
        )

    print(f"Collection '{COLLECTION_NAME}' created successfully.")

if __name__ == "__main__":
    create_collection()
