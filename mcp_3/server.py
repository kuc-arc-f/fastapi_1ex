from mcp.server.fastmcp import FastMCP
import chromadb
import ollama
import uuid

# サーバーの初期化
mcp = FastMCP("My Local Server")
DB_PATH = '/tmp/my_chroma_db'

#
#
#
def search(query):
    client = chromadb.PersistentClient(path=DB_PATH) 
    #print("ChromaDB クライアントを初期化しました。")   
    # コレクション名の指定
    collection_name = "my_document_collection"
    # コレクションの作成または取得
    # get_or_create を使うと、既に存在すればそれを取得し、なければ新しく作成します
    collection = client.get_or_create_collection(name=collection_name)


    # 検索クエリ
    query_text = query
    print("query:" + query_text)
    response = ollama.embeddings(prompt=query_text, model="qwen3-embedding:0.6b")
    query_vector = response["embedding"]
    query_vec_str = [str(n) for n in query_vector]
    len_str = str(len(query_vec_str))

    #最も関連性の高いドキュメントを取得
    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=1
    )
    # 結果をdistancesでソートして表示
    documents = results['documents'][0]
    distances = results['distances'][0]

    # (distance, document)のペアを作成してソート
    sorted_results = sorted(zip(distances, documents))    

    ouStr = "" 
    matches = ""
    for distance, doc in sorted_results:
        #print(f"\nベクトル距離: {distance:.2f}")
        #print(f"document: {doc}")
        ouStr += doc + "\n\n"

    #print("out.len=" + str(len(ouStr))) 
    print("out.len=" + str(len(ouStr))) 
    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query_text}"
    else:
        matches = f"user query: {query_text}"
    #print(matches)

    sendMessage = f"日本語で回答して欲しい。\n "
    sendMessage += f"概要して欲しい。\n\n {matches} \n"    
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
