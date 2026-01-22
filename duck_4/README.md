# duck_4

 Version: 0.9.1

 date    : 2026/01/21

 update :

***

DuckDb RAG , LM Studio example

* lfm2.5-1.2b-instruct , LM Studio
* embedding: qwen3-embedding:0.6b ollama
* Python 3.13.4

***
### related

https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF/tree/main

***
### setup
```
python -m venv venv
.\venv\Scripts\activate

pip install requests
pip install duckdb
pip install uuid
pip install ollama
pip install langchain-text-splitters
```

***
* vector data add

```
python embed.py
```

* RAG Search

```
python search.py hello
```

***
### blog

https://zenn.dev/knaka0209/scraps/2cf45419d0afcd

***
