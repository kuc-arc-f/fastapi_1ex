# rag_1

 Version: 0.9.1

 Author  :

 date    : 2025/12/07
 
 update :

***

fastAPI , RAG example

* Python 3.13.4

***
* .env

```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-key
```
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
* front

```
npm i
npm run build
```

* open: http://localhost:8080/

***
* test-code: test.js

```js

const start = async function() {
  try{
      const response = await fetch("http://localhost:8080/api/rag_search", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'abcdef-123456',
      },
      body: JSON.stringify({query: "春夏秋冬"}),
    });
    if (!response.ok) {
      const text = await response.text();
      console.log(text);
      throw new Error('Failed to create item');
    }else{
      console.log("OK");
      const json = await response.json();
      console.log(json);
    }
  }catch(e){console.log(e)}
}
start();


```

***
### blog

https://zenn.dev/knaka0209/scraps/5c624997da4d09

***
