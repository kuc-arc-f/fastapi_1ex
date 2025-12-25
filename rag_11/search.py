from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import random
import uuid
import os
import glob
from google import genai
from dotenv import load_dotenv

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# .envファイルから環境変数を読み込む
load_dotenv()

COLLE_NAME="my_document"

#
#
#
def search():
    query_text = "二十四節季"
    client = genai.Client(api_key=GOOGLE_API_KEY)

    clientQdrant = QdrantClient(
        url="http://localhost:6333"
    )

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
        search_result = clientQdrant.query_points(
            collection_name=COLLE_NAME,
            query=embedding.values,  # 生成したEmbedding（ベクトル）
            limit=2,  # 上位5件を取得
            #with_payload=True  # メタデータも一緒に取得
        )

        for hit in search_result.points:
            #print(f"ID: {hit.id},  Data: {hit.payload}")
            print(f"ID: {hit.id},  content: {hit.payload["content"]}")
            ouStr += hit.payload["content"] + "\n\n"

    print("out.len=" + str(len(ouStr))) 
    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query_text}"
    else:
        matches = f"user query: {query_text}"

    sendMessage = f"日本語で回答して欲しい\n {matches} \n"
    print(sendMessage)
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



