import chromadb
import ollama
import uuid

#
#
#
def search():
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
    # クエリーテキストに対して埋め込みを生成
    response = ollama.embeddings(prompt=query_text, model="qwen3-embedding:0.6b")

    #最も関連性の高いドキュメントを取得
    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=2
    )
    # 結果をdistancesでソートして表示
    documents = results['documents'][0]
    distances = results['distances'][0]

    # (distance, document)のペアを作成してソート
    sorted_results = sorted(zip(distances, documents))

    print("検索結果 (ベクトル距離が近い順):")
    ouStr = "" 
    matches = ""
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
    res = ollama.chat(
        model="gemma3:4b",
        messages=[{'role': 'user', 'content': sendMessage}],
        options={
            'num_predict': 200,
            'num_ctx': 1024
        }
    )
    print(res['message']['content'])
    return

#
#
#
if __name__ == "__main__":
    search()

