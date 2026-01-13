import duckdb
import ollama
import uuid

conn = duckdb.connect(database='vector.db')

#
#
#
def search():
    conn.execute("INSTALL vss; LOAD vss;")

    # 検索クエリ
    query_text = "二十四節季"
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
    LIMIT 2;
    """

    resp = conn.execute(select_sql, [query_vec_str]).fetchall()
    #print(resp)
    ouStr = "" 
    matches = ""
    for row in resp:
        print(row[1])
        print("sim:"+ str(row[3])) 
        ouStr += row[1] + "\n\n"   

    print("out.len=" + str(len(ouStr))) 

    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query_text}"
    else:
        matches = f"user query: {query_text}"
    #print(matches)

    sendMessage = f"日本語で回答して欲しい\n {matches} \n"
    print(sendMessage)
    res = ollama.chat(
        model="qwen3:1.7b",
        messages=[{'role': 'user', 'content': sendMessage}],
    )
    print(res['message']['content'])
    return

#
#
#
if __name__ == "__main__":
    search()

