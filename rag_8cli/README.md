# rag_8cli

 Version: 0.9.1

 Author  :

 date    : 2025/12/18
 
 update :

***

python , RAG example

* ChromaDB use
* embedding: gemini-embedding-001
* model: gemma3 , GEMINI-API
* Python 3.13.4

***
### setup

* .env
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-key
```

***
* windows
* venv install
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

* pip install

```
pip install google-genai
pip install chromadb uuid
pip install langchain-text-splitters
pip install python-dotenv
```
***
* vector data add
```
python init_db.py
python embed.py
```

***
* search

```
python search.py
```
***
### blog

https://zenn.dev/link/comments/12f74a8be3040b

***
