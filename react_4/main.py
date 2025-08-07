from fastapi import FastAPI, Form, Response, Request, HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from typing import List

# SQLAlchemy関連のインポート
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Pydanticモデル（スキーマ）のインポート
from pydantic import BaseModel

# 固定ユーザー名・パスワード
USERNAME = "admin"
PASSWORD = "1111"
COOKIE_NAME = "fastapi_auth"
COOKIE_VALUE = "authenticated"

# --- FastAPIアプリケーションの初期化 ---

app = FastAPI()

# public フォルダを静的ファイルとしてマウント
# /static というURLパスで public フォルダの内容にアクセスできるようになります。
app.mount("/static", StaticFiles(directory="public"), name="static")

# Jinja2Templates を使用してHTMLテンプレートをレンダリングする場合
# templates フォルダにHTMLファイルがあることを想定
templates = Jinja2Templates(directory="templates")


def is_logged_in(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if token != COOKIE_VALUE:
        raise HTTPException(status_code=401, detail="Not authenticated")

@app.get("/login", response_class=HTMLResponse)
def login_form():
    return """
    <form action="/login" method="post">
        ユーザー名: <input type="text" name="username"><br>
        パスワード: <input type="password" name="password"><br>
        <input type="submit" value="ログイン">
    </form>
    """

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key=COOKIE_NAME)
    return response

@app.post("/login")
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    if username == USERNAME and password == PASSWORD:
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(key=COOKIE_NAME, value=COOKIE_VALUE, httponly=True)
        return response
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/foo", response_class=HTMLResponse)
async def read_foo(request: Request):
    logged_in = request.cookies.get(COOKIE_NAME) == COOKIE_VALUE
    if logged_in == False:
        return RedirectResponse(url="/login")
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Static Files</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    </head>
    <body>
        <div id="app"></div>
        <script type="module" src="/static/client.js"></script>
    </body>
    </html>
    """

@app.get("/hoge")
def read_hoge(request: Request):
    logged_in = request.cookies.get(COOKIE_NAME) == COOKIE_VALUE
    if logged_in == False:
        return RedirectResponse(url="/login")
    return {"message": "ログイン済みユーザーだけが見れるページ"}

@app.get("/bar")
def read_bar():
    return {"bar": "bar-2"}
