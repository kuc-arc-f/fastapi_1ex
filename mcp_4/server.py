from mcp.server.fastmcp import FastMCP
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import ollama
import uuid

# サーバーの初期化
mcp = FastMCP("My Local Server")
COLLE_NAME="my_document"

#
#
#
def search(query):
    clientQdrant = QdrantClient(
        url="http://localhost:6333"
    )

    # 検索クエリ
    query_text = query
    #print("query:" + query_text)
    response = ollama.embeddings(prompt=query_text, model="qwen3-embedding:0.6b")
    query_vector = response["embedding"]

    ouStr = "" 
    matches = ""
    if len(query_vector) > 0:
        search_result = clientQdrant.query_points(
            collection_name=COLLE_NAME,
            query=query_vector,  # 生成したEmbedding（ベクトル）
            limit=2,  # 上位n件を取得
        )

        for hit in search_result.points:
            #print(f"ID: {hit.id},  content: {hit.payload["content"]}")
            ouStr += hit.payload["content"] + "\n\n"

    #print("out.len=" + str(len(ouStr))) 
    print("out.len=" + str(len(ouStr))) 
    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query_text}"
    else:
        matches = f"user query: {query_text}"

    sendMessage = f"日本語で回答して欲しい\n {matches} \n"
    #print(sendMessage)
    return sendMessage


#検索文字から、RAG検索 結果を返す。
# --- Tools: LLMが実行できる「関数」の定義 ---
@mcp.tool()
def rag_search(query: str) -> str:
    """検索文字から、RAG検索 結果を返す。"""
    resp = search(query)
    return resp


if __name__ == "__main__":
    # stdio通信モードで実行（Claude Desktopなどから呼び出す際に標準的な方式）
    mcp.run()
