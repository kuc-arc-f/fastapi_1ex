# rag_2

 Version: 0.9.1

 Author  :

 date    : 2025/12/07
 
 update :

***

fastAPI , remote MCP Server RAG example

* GEMINI-CLI use
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
* settings.json , GEMINI-CLI
```
"mcpServers": {
    "rag-mcp-server-2": {
        "httpUrl": "http://localhost:8000/mcp"
    }
}
```
***
* test-code: test.js

```js

const start = async function() {
  try{
      const item = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
          "name": "rag_search",
          "arguments": {"query": "二十四節季"}
        },
        "id": 2
      }    
      const response = await fetch("http://localhost:8000/mcp", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': '123',
      },
      body: JSON.stringify(item),
    });
    if (!response.ok) {
      const text = await response.text();
      console.log(text);
      throw new Error('Failed to create item');
    }else{
      console.log("OK");
      const json = await response.json();
      console.log(json);
      console.log(json.result.content[0].text);
    }
  }catch(e){console.log(e)}
}
start();


```
***
### blog

https://zenn.dev/knaka0209/scraps/0104ea528d8acc

***
