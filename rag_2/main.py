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

app = FastAPI()

@app.post("/mcp")
async def handle_mcp(request: Request):
    req = await request.json()
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": 'fastapi-mcp-1',
                    "version": '1.0.0'
                }
            }
        }        

    # --------------------------
    # tool.call の処理
    # --------------------------
    if method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "search":
            query = args.get("query", "")
            result = {
                "results": [
                    {"title": "Dummy Result 1", "q": query},
                    {"title": "Dummy Result 2", "q": query}
                ]
            }

        elif tool_name == "rag_search":
            query = args.get("query", "")
            resp = rag_search(query)
            inputStr = "日本語で、回答して欲しい。\n" + resp
            result = {
                "content": [
                    {
                        "type": "text",
                        "text": inputStr
                    }
                ]
            } 

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": "Tool not found"},
            }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": result,
        }

    # --------------------------
    # tools/list
    # --------------------------
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": 'rag_search',
                        "description": '入力文字から、検索結果を返す',
                        "inputSchema": {
                        "type": 'object',
                        "properties": {
                            "query": {
                                "type": 'string',
                                "description": '入力文字'
                            }
                        },
                        "required": ['query']
                        }
                    },

                ]
            }
        }

    # --------------------------
    # fallback
    # --------------------------
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": "Method not found"},
    }

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
def rag_search(query):
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
    print(matches)

    return matches
