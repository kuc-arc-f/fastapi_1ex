import chromadb
import json
import os
import ollama
from fastapi import FastAPI, Request
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Pydanticモデル（スキーマ）のインポート
from pydantic import BaseModel

# 4. モデルクラスが継承するBaseクラスを定義
Base = declarative_base()

class SearchRequest(BaseModel):
    query: str

app = FastAPI()

# public フォルダを静的ファイルとしてマウント
# /static というURLパスで public フォルダの内容にアクセスできるようになります。
app.mount("/static", StaticFiles(directory="public"), name="static")

# Jinja2Templates を使用してHTMLテンプレートをレンダリングする場合
# templates フォルダにHTMLファイルがあることを想定
templates = Jinja2Templates(directory="templates")

#
#
#
def search(query):
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

    # クエリーテキストに対して埋め込みを生成
    response = ollama.embeddings(prompt=query, model="qwen3-embedding:0.6b")

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
    #print(ouStr)
    print("out.len=" + str(len(ouStr))) 
    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query}"
    else:
        matches = f"user query: {query}"

    return matches

#
#
#
@app.post("/api/rag_search")
def rag_search(item: SearchRequest):
    print("query=" + item.query)
    query = item.query

    matches = search(query)
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
    #print(res['message']['content'])
    return {
        "status": "success",
        "result": res['message']['content']
    }    

#
#
#
@app.get("/", response_class=HTMLResponse)
async def home_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Static Files</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        <link href="/static/main.css" rel="stylesheet"/>
    </head>
    <body>
        <div id="app"></div>
        <script type="module" src="/static/client.js"></script>
    </body>
    </html>
    """