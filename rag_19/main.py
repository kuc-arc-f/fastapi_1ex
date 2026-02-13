import os
import ollama
from fastapi import FastAPI, Request
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pgvector.psycopg2 import register_vector
import psycopg2
import json
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
def search_similar(embedding, top_k=5):
    # PostgreSQL 接続
    conn = psycopg2.connect(
        dbname="mydb",
        user="root",
        password="admin",
        host="localhost",
        port=5432
    )

    # pgvector を psycopg2 に登録
    register_vector(conn)

    # -- コサイン距離をコサイン類似度 (1 - 距離) に変換し、similarityとして取得
    # -- 類似度が高い順（降順）に並び替え
    SQL_QUERY = """
    SELECT
        id,
        content,
        embedding,
        1 - (embedding <=> %s) AS cosine_similarity
    FROM
        documents
    ORDER BY
        cosine_similarity DESC
    LIMIT 3;
    """

    query_vector_str = json.dumps(embedding)
    with conn.cursor() as cur:
        cur.execute(SQL_QUERY, (query_vector_str,))
        return cur.fetchall()

#
#
#
@app.post("/api/rag_search")
def rag_search(item: SearchRequest):
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

    matches = ""
    ouStr = "" 
    rows = search_similar(vec, 3)

    for row in rows:
        ouStr += row[1]+ "\n\n"
    print("out.len=" + str(len(ouStr))) 

    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query}"
    else:
        matches = f"user query: {query}"
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