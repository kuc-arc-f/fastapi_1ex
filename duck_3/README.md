# duck_3

 Version: 0.9.1

 date    : 2026/01/20

 update :

***

DuckDb RAG , ollama example

* LFM2.5-Thinking , Ollama
* embedding: qwen3-embedding:0.6b
* Python 3.13.4

***
### related

https://ollama.com/library/lfm2.5-thinking

***
### setup

```
python -m venv venv
.\venv\Scripts\activate

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

https://zenn.dev/knaka0209/scraps/d66fb0a5504a28

***
