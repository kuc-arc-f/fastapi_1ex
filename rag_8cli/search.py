import chromadb
import uuid
import os
import glob
from google import genai
from dotenv import load_dotenv

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# .envファイルから環境変数を読み込む
load_dotenv()

#
#
#
def search():
    client = genai.Client(api_key=GOOGLE_API_KEY)
    # クライアントの初期化 (ローカルにデータベースファイルを作成)
    # インメモリで実行する場合は chromadb.Client() を使用します
    client = chromadb.PersistentClient(path="./my_chroma_db") 
    print("ChromaDB クライアントを初期化しました。")

    # コレクション名の指定
    collection_name = "my_document_collection"

    # コレクションの作成または取得
    # get_or_create を使うと、既に存在すればそれを取得し、なければ新しく作成します
    collection = client.get_or_create_collection(name=collection_name)

    print(f"コレクション '{collection_name}' を作成/取得しました。")

    # 検索クエリ
    query_text = "二十四節季"
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
        #最も関連性の高いドキュメントを取得
        results = collection.query(
            query_embeddings=[embedding.values],
            n_results=2
        )
        # 結果をdistancesでソートして表示
        documents = results['documents'][0]
        distances = results['distances'][0]

        # (distance, document)のペアを作成してソート
        sorted_results = sorted(zip(distances, documents))
        print("検索結果 (ベクトル距離が近い順):")
        for distance, doc in sorted_results:
            print(f"\nベクトル距離: {distance:.2f}")
            print(f"document: {doc}")
            ouStr += doc + "\n\n"

    print("out.len=" + str(len(ouStr))) 
    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query_text}"
    else:
        matches = f"user query: {query_text}"
    #print(matches)

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

