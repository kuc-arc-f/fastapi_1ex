from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import random

COLLE_NAME="my_document"
EMBED_SIZE=1024

client = QdrantClient(
    url="http://localhost:6333"
)

client.recreate_collection(
    collection_name=COLLE_NAME,
    vectors_config={
        "size": EMBED_SIZE,
        "distance": "Cosine",  # Cosine / Dot / Euclid
    }
)