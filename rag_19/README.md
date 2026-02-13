# rag_19

 Version: 0.9.1

 date    : 2026/02/12
 
 update :

***

RAG example , ChromaDB use

* Github Copilot SDK , python
* embedding: qwen3-embedding:0.6b , ollama
* model: gpt-4.1
* Python 3.13.4

***
### setup

* windows
```
python -m venv venv
.\venv\Scripts\activate

pip install ollama
pip install langchain-text-splitters
pip install chromadb uuid
pip install github-copilot-sdk

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

***
