import weaviate
from weaviate.connect import ConnectionParams
from weaviate.classes.config import Property, DataType

COLLECT_NAME = "document"
client = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_url(
        "http://localhost:8080",
        grpc_port=50051
    )
)

client.connect()
# 接続確認
print(client.is_ready())

client.collections.create(
    name=COLLECT_NAME,
    properties=[
        Property(name="content", data_type=DataType.TEXT),
        Property(name="category", data_type=DataType.TEXT),
    ]
)

# 処理が終わったら閉じる（または context manager を使用）
client.close()

