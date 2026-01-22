import os
import ollama
import duckdb
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

API_URL = "http://localhost:1234/v1/chat/completions"

class SearchRequest(BaseModel):
    query: str

app = FastAPI()
DB_FILE="/tmp/vector.db"

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
def rag_search(item: SearchRequest):
    conn = duckdb.connect(database=DB_FILE)
    conn.execute("INSTALL vss; LOAD vss;")
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

    select_sql = """SELECT 
    id, 
    text, 
    vector, 
    array_cosine_similarity(vector, CAST(? AS FLOAT[1024])) AS similarity
    FROM embeddings
    ORDER BY similarity DESC
    LIMIT 1;
    """

    resp = conn.execute(select_sql, [query_vec_str]).fetchall()
    #print(resp)

    matches = ""
    ouStr = "" 
    for row in resp:
        print(row[1])
        print("sim:"+ str(row[3])) 
        ouStr += row[1] + "\n\n"   

    print("out.len=" + str(len(ouStr)))     
    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query}\n"
    else:
        matches = f"user query: {query}"
    #print(matches)

    sendMessage = f"日本語で回答して欲しい\n"
    sendMessage += f"要約して欲しい\n\n {matches} \n"
    print(sendMessage)    
    payload = {
        "model": "lfm2.5-1.2b-instruct",
        "messages": [
            {"role": "user", "content": sendMessage}
        ],
        "temperature": 0.7
    }
    res = requests.post(API_URL, json=payload)
    print(res.json()["choices"][0]["message"]["content"])
    out = res.json()["choices"][0]["message"]["content"]
    return {
        "status": "success",
        "result": out
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