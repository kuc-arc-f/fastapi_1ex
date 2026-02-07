import asyncio
import duckdb
import ollama
import uuid
import sys
from copilot import CopilotClient

conn = duckdb.connect(database='vector.db')

#
#
#
def search(query):
    conn.execute("INSTALL vss; LOAD vss;")

    # 検索クエリ
    query_text = query
    print("query:" + query_text)
    # クエリーテキストに対して埋め込みを生成
    response = ollama.embeddings(prompt=query_text, model="qwen3-embedding:0.6b")
    query_vector = response["embedding"]
    query_vec_str = [str(n) for n in query_vector]

    select_sql = """SELECT 
    id, 
    text, 
    vector, 
    array_cosine_similarity(vector, CAST(? AS FLOAT[1024])) AS similarity
    FROM embeddings
    ORDER BY similarity DESC
    LIMIT 1;
    """

    resp = conn.execute(select_sql, [query_vec_str]).fetchall()
    #print(resp)
    ouStr = "" 
    matches = ""
    for row in resp:
        #print(row[1])
        print("sim:"+ str(row[3])) 
        ouStr += row[1] + "\n\n"   

    print("out.len=" + str(len(ouStr))) 

    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query_text}"
    else:
        matches = f"user query: {query_text}"
    #print(matches)

    sendMessage = f"日本語で回答して欲しい\n"
    sendMessage += f"要約して欲しい\n\n {matches} \n"
    print(sendMessage)
    return sendMessage

#
#
#
async def send_text(query):
    client = CopilotClient()
    await client.start()

    session = await client.create_session({"model": "gpt-4.1"})
    response = await session.send_and_wait({"prompt": query})

    print(response.data.content)

    await client.stop()
#
#
#
if __name__ == "__main__":
    args = sys.argv

    print(f"実行ファイル名: {args[0]}")
    if len(args) > 1:
        print(f"最初の引数: {args[1]}")
        #print(f"すべての引数: {args[1:]}")
        query = search(args[1])
        asyncio.run(send_text(query))
    else:
        print(f"error argment nothing, ex: python search.py hello")


