# mcp_2

 Version: 0.9.1

 Author  :

 date    : 2026/01/12
 
 update :

***

RAG example , DuckDB

* embedding: qwen3-embedding:0.6b Ollama
* Python 3.13.4
* GEMINI-CLI use

***
* vector data add

https://github.com/kuc-arc-f/fastapi_1ex/tree/main/duck_2

***
### setup

* pip install
```
pip install mcp fastmcp
pip install duckdb uuid
pip install ollama

```

***
* settings.json , GEMINI-CLI

```
  "mcpServers": {
    "python-rag-search-1": {
      "command": "python",
      "args": [
        "/path/mcp_2/server.py"
      ],
      "env": {
        "hoge": ""
      }
    }    
  },
```

***
### blog

***
