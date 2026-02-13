import asyncio
import chromadb
import os
import ollama
import uuid
from copilot import CopilotClient
from fastapi import FastAPI, Request
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import requests
import sys

# Pydanticモデル（スキーマ）のインポート
from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str

class AddRequest(BaseModel):
    content: str

class EditDeleteRequest(BaseModel):
    id: str

app = FastAPI()
DB_PATH="./my_chroma_db"
collection_name = "my_document_collection"

# public フォルダを静的ファイルとしてマウント
# /static というURLパスで public フォルダの内容にアクセスできるようになります。
app.mount("/static", StaticFiles(directory="public"), name="static")

# Jinja2Templates を使用してHTMLテンプレートをレンダリングする場合
# templates フォルダにHTMLファイルがあることを想定
templates = Jinja2Templates(directory="templates")

#
#
#
@app.post("/api/rag_search")
async def rag_search(item: SearchRequest):
    client = chromadb.PersistentClient(path=DB_PATH) 
    print("ChromaDB クライアントを初期化しました。")
    print("query=" + item.query)
    query = item.query

    print("query=" + query)
    
    embedding = ollama.embeddings(
        model="qwen3-embedding:0.6b",
        prompt=query
    )
    vec = embedding["embedding"]

    print(len(vec))
    print(vec[:5])   

    query_vector = embedding["embedding"]
    query_vec_str = [str(n) for n in query_vector]

    collection = client.get_or_create_collection(name=collection_name)
    print(f"コレクション '{collection_name}' を作成/取得しました。")

    #最も関連性の高いドキュメントを取得
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=1
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
    #print(resp)
    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query}\n"
    else:
        matches = f"user query: {query}"
    #print(matches)

    sendMessage = f"日本語で回答して欲しい\n"
    sendMessage += f"要約して欲しい\n\n {matches} \n"
    print(sendMessage) 
    newMessage = await send_text(sendMessage) 
    return {
        "status": "success",
        "result": newMessage
    } 
     
#
#
#
async def send_text(query):
    client = CopilotClient()
    await client.start()

    session = await client.create_session({"model": "gpt-4.1"})
    response = await session.send_and_wait({"prompt": query})

    print(response.data.content)

    await client.stop()
    return response.data.content


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
