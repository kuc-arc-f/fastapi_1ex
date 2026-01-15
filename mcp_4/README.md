# mcp_4

 Version: 0.9.1

 Author  :

 date    : 2026/01/12
 
 update :

***

RAG example , Qdrant

* embedding: qwen3-embedding:0.6b Ollama
* Python 3.13.4
* GEMINI-CLI use


***
### setup

* pip install
```
pip install mcp fastmcp
pip install ollama
pip install langchain-text-splitters
pip install qdrant-client uuid

```

***
* initial collection
```
python init_db.py
```

***
* vector data add
```
python embed.py
```

***
* settings.json , GEMINI-CLI
```
  "mcpServers": {
    "python-rag-search-4": {
      "command": "python",
      "args": [
        "/path/mcp_4/server.py"
      ],
      "env": {
        "hoge": ""
      }
    }    
  },
```

***
### blog

https://zenn.dev/knaka0209/scraps/e1c65314f077e9

***
