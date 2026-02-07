# rag_18

 Version: 0.9.1

 Author  :

 date    : 2026/02/07
 
 update :

***

fastAPI DuckDB , RAG example

* Github Copilot SDK , python
* gpt-4.1
* embedding: qwen3-embedding:0.6b , ollama
* Python 3.13.4

***
* vector data add

https://github.com/kuc-arc-f/fastapi_1ex/tree/main/duck_7

***
### setup

* windows
```
python -m venv venv
.\venv\Scripts\activate

pip install fastapi uvicorn sqlalchemy
pip install "fastapi[all]" python-multipart
pip install requests
pip install duckdb uuid
pip install ollama
pip install github-copilot-sdk

uvicorn main:app --reload --port 8000
```

***
* front

```
npm i
npm run build
```

***
### blog

https://zenn.dev/link/comments/b8a36e48a19ffe

***
