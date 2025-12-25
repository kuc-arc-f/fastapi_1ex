# rag_11

 Version: 0.9.1

 Author  :

 date    : 2025/12/25
 
 update :

***

RAG example , Qdrant

* embedding: gemini-embedding-001
* model: gemma3-27b
* Python 3.13.4

***
### setup

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
pip install python-dotenv
pip install langchain-text-splitters
pip install qdrant-client
```

* .env
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-key
```
***
* data path: ./data

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

https://zenn.dev/link/comments/0414c024bb8499

***
