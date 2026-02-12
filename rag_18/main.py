import asyncio
import duckdb
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
DB_FILE="vector.db"

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

    #
    copilot_client = CopilotClient()
    await copilot_client.start()

    session = await copilot_client.create_session({"model": "gpt-4.1"})
    response = await session.send_and_wait({"prompt": sendMessage})
    print(response.data.content)

    await copilot_client.stop()    

    return {
        "status": "success",
        "result": response.data.content
    }        

#
#
#
@app.post("/api/edit_list")
async def edit_list(item: SearchRequest):
    conn = duckdb.connect(database=DB_FILE)
    conn.execute("INSTALL vss; LOAD vss;")
    print("query=" + item.query)
    query = item.query

    print("query=" + query)
    if query == "":
        select_sql = """SELECT 
        id, 
        text, 
        FROM embeddings
        ORDER BY id DESC
        LIMIT 100;
        """
    else:
        select_sql = """SELECT id, text 
        FROM embeddings
        """
        select_sql += f" WHERE text LIKE '%{query}%' LIMIT 100"
    print("select_sql=" + select_sql)

    resp = conn.execute(select_sql).fetchall()
    matches = ""
    ouStr = "" 
    #print(resp)

    return {
        "status": "success",
        "result": resp
    }

#
#
#
@app.post("/api/edit_create")
async def edit_create(item: AddRequest):
    conn = duckdb.connect(database=DB_FILE)
    conn.execute("INSTALL vss; LOAD vss;")
    print("query=" + item.content)
    in_text = item.content

    print("in_text=" + in_text)
    
    embedding = ollama.embeddings(
        model="qwen3-embedding:0.6b",
        prompt=in_text
    )
    vec = embedding["embedding"]

    print(len(vec))
    print(vec[:5])   

    add_vector = embedding["embedding"]
    newUID = str(uuid.uuid4())
    insert_sql = """
    INSERT INTO embeddings 
        (id, text, vector) VALUES 
        (?, ?, CAST(? AS FLOAT[1024]))
    """
    conn.execute(insert_sql , (newUID , in_text, add_vector))
    return {
        "status": "success",
        "result": ""
    }  

#
#
#
@app.post("/api/edit_delete")
async def edit_delete(item: EditDeleteRequest):
    conn = duckdb.connect(database=DB_FILE)
    conn.execute("INSTALL vss; LOAD vss;")
    print("id=" + item.id)
    id = item.id

    delete_sql = """
    DELETE FROM embeddings WHERE id = $1
    """
    conn.execute(delete_sql , [id])

    return {
        "status": "success",
        "result": ""
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

@app.get("/edit", response_class=HTMLResponse)
async def edit_page():
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