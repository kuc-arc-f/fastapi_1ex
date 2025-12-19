import asyncio
import chromadb
import json
import os
import ollama
from dotenv import load_dotenv
from google import genai
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

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# .envファイルから環境変数を読み込む
load_dotenv()

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
def search(query, embedding):
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
    ouStr = "" 
    for distance, doc in sorted_results:
        print(f"\nベクトル距離: {distance:.2f}")
        print(f"document: {doc}")
        ouStr += doc + "\n\n"

    #return ouStr
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

    matches = ""
    genClient = genai.Client(api_key=GOOGLE_API_KEY)
    result = genClient.models.embed_content(
        model="gemini-embedding-001",
        contents=query)

    if len(result.embeddings) > 0:
        embedding = result.embeddings[0]
        print("v.len="+ str(len(embedding.values)))  

    matches = search(query, embedding)
    sendMessage = f"日本語で回答して欲しい\n {matches} \n"
    print(sendMessage)

    #LLM gemma
    genClient = genai.Client(api_key=GOOGLE_API_KEY)

    response = genClient.models.generate_content(
        model="gemma-3-27b-it",
        contents=sendMessage,
    )    
    print(response.text)  
    return {
        "status": "success",
        "result": response.text
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