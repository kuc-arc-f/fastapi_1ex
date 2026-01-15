# mcp_3

 Version: 0.9.1

 Author  :

 date    : 2026/01/12
 
 update :

***

RAG example , ChromaDB

* embedding: qwen3-embedding:0.6b Ollama
* Python 3.13.4
* GEMINI-CLI use

***
* vector data add

https://github.com/kuc-arc-f/fastapi_1ex/tree/main/rag_6

***
### setup

* pip install
```
pip install mcp fastmcp
pip install ollama
pip install langchain-text-splitters
pip install chromadb uuid

```
***
* settings.json , GEMINI-CLI
```
  "mcpServers": {
    "python-rag-search-3": {
      "command": "python",
      "args": [
        "/path/mcp_3/server.py"
      ],
      "env": {
        "hoge": ""
      }
    }    
  },
```

***
### blog

https://zenn.dev/knaka0209/scraps/a82508b741cc4b

***
