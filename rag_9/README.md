# rag_9

 Version: 0.9.1

 Author  :

 date    : 2025/12/18
 
 update :

***

fastAPI , RAG example

* ChromaDB use
* embedding: gemini-embedding-001
* model: gemma3
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
