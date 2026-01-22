# rag_16

 Version: 0.9.1

 Author  :

 date    : 2026/01/12
 
 update :

***

fastAPI DuckDB , RAG example

* model: LFM2.5-1.2B-Instruct , LM Studio
* embedding: qwen3-embedding:0.6b , ollama
* Python 3.13.4

***
* vector data add

https://github.com/kuc-arc-f/fastapi_1ex/tree/main/duck_2

***
### related

https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF/tree/main

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

https://zenn.dev/link/comments/a5cf9ce9b06110

***
