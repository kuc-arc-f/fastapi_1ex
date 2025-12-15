# rag_7

 Version: 0.9.1

 Author  :

 date    : 2025/12/15
 
 update :

***

fastAPI , RAG example

* ChromaDB use
* model: gemma3:4b
* embedding: qwen3-embedding:0.6b
* Python 3.13.4

***
### setup

* windows
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

uvicorn main:app --reload --port 8080
```

***
* vector data add
```
python init_db.py
python embed.py
```

***
* front
```
npm i
npm run build
```
***
### blog

***
