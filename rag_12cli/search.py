import glob
import random
import uuid
import os
import weaviate
from google import genai
from dotenv import load_dotenv
from weaviate.connect import ConnectionParams
from weaviate.classes.config import Property, DataType
from weaviate.classes.query import MetadataQuery
import weaviate.classes.config as Configure

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# .envファイルから環境変数を読み込む
load_dotenv()

COLLECT_NAME = "document"
clientWeaviate = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_url(
        "http://localhost:8080",
        grpc_port=50051
    )
)
clientWeaviate.connect()
# 接続確認
print(clientWeaviate.is_ready())
#
#
#
def search():
    query_text = "二十四節季"

    if not clientWeaviate.collections.exists(COLLECT_NAME):
        print("not-exist-COLLECT")    
        clientWeaviate.close()

    collection = clientWeaviate.collections.get(COLLECT_NAME)

    print("query:" + query_text)
    ouStr = "" 
    matches = ""
    # クエリーテキストに対して埋め込みを生成
    client = genai.Client(api_key=GOOGLE_API_KEY)
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query_text)

    if len(result.embeddings) > 0:
        embedding = result.embeddings[0]
        query_vector = embedding.values 
        # 2. 指定したベクトルで近傍検索を実行
        response = collection.query.near_vector(
            near_vector=query_vector,
            limit=2,                             # 取得件数
            return_metadata=MetadataQuery(distance=True) # 距離（近さ）も取得する場合
        )
        # 3. 結果の表示
        for obj in response.objects:
            print(f"content: {obj.properties.get('content')}")
            print(f"距離: {obj.metadata.distance}") # 値が小さいほど似ている
            print("-" * 20)       
            ouStr += obj.properties.get('content') + "\n\n" 

    clientWeaviate.close()

    print("out.len=" + str(len(ouStr))) 
    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query_text}"
    else:
        matches = f"user query: {query_text}"

    sendMessage = f"日本語で回答して欲しい\n {matches} \n"
    print(sendMessage)
    #send-LLM
    client = genai.Client(api_key=GOOGLE_API_KEY)

    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=sendMessage,
    )

    print(response.text)    
    return

#
#
#
if __name__ == "__main__":
    search()



