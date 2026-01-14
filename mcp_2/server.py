from mcp.server.fastmcp import FastMCP
import duckdb
import ollama
import uuid

# サーバーの初期化
mcp = FastMCP("My Local Server")
DB_PATH = '/tmp/vector.db'

#
#
#
def search(query):
    conn = duckdb.connect(database=DB_PATH)
    conn.execute("INSTALL vss; LOAD vss;")

    # 検索クエリ
    query_text = query
    print("query:" + query_text)
    response = ollama.embeddings(prompt=query_text, model="qwen3-embedding:0.6b")
    query_vector = response["embedding"]
    query_vec_str = [str(n) for n in query_vector]
    len_str = str(len(query_vec_str))

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
        #print(row[1])
        #print("sim:"+ str(row[3])) 
        ouStr += row[1] + "\n\n"  
    #print(sendMessage)
    len_str = str(len(ouStr))
    if len(ouStr) > 0:
        matches = f"context: {ouStr}\n user query: {query_text}"
    else:
        matches = f"user query: {query_text}"

    sendMessage = f"日本語で回答して欲しい\n {matches} \n"
    #print(sendMessage)    
    return sendMessage


#検索文字から、RAG検索 結果を返す。
# --- Tools: LLMが実行できる「関数」の定義 ---
@mcp.tool()
def rag_search(query: str) -> str:
    """検索文字から、RAG検索 結果を返す。"""
    resp = search(query)
    return resp

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """2つの数値を合計します。"""
    return a + b

@mcp.tool()
def get_system_status() -> str:
    """ローカルマシンのステータスを返します。"""
    return "All systems operational."

# --- Resources: LLMが参照できる「データ」の定義 ---
@mcp.resource("config://settings")
def get_config() -> str:
    """アプリケーションの設定情報を返します。"""
    return "Mode: Development\nVersion: 1.0.0"

if __name__ == "__main__":
    # stdio通信モードで実行（Claude Desktopなどから呼び出す際に標準的な方式）
    mcp.run()
