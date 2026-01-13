import duckdb
import ollama
import uuid
import glob
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

folder_path = "./data"
conn = duckdb.connect(database='vector.db')

# スプリッターの初期化
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # 1チャンクあたりの文字数（目安）
    chunk_overlap=100,    # 前後のチャンクと重複させる文字数（文脈維持のため）
    length_function=len, # 長さを測る関数（通常はlen）
    separators=["\n\n", "\n", "。", " ", ""] # 分割する優先順位
    # is_separator_regex=False,
)

#
#
#
def read_file():
    # INSTALL vss; LOAD vss;
    conn.execute("INSTALL vss; LOAD vss;")

    create_sql = """
    CREATE TABLE IF NOT EXISTS embeddings (
        id TEXT PRIMARY KEY,
        text VARCHAR,
        vector FLOAT[1024]
    );
    """
    #print(create_sql)
    conn.execute(create_sql)

    data = []
    contData = []
    for file_path in glob.glob(os.path.join(folder_path, "*.txt")):
        with open(file_path, "r", encoding="utf-8") as f:
            targetContent = f.read()
            # 分割実行
            chunks = text_splitter.create_documents([targetContent])
            for i, chunk in enumerate(chunks):
                print(f"Chunk {i}: {chunk.page_content}")
                data.append({
                    "filename": os.path.basename(file_path),
                    "content": chunk.page_content,
                })
                contData.append(chunk.page_content)

    #
    for i, d in enumerate(data):
        print(f"data:{str(i)} \n")
        content_str = d["content"]
        #print(f"{d["content"]}\n")
        print(f"{content_str}\n")
        response = ollama.embeddings(model="qwen3-embedding:0.6b", prompt=content_str)
        embedding = response["embedding"]
        print("embedding.len=" + str(len(embedding)) )
        add_vector = embedding
        newUID = str(uuid.uuid4())
        insert_sql = """
        INSERT INTO embeddings 
            (id, text, vector) VALUES 
            (?, ?, CAST(? AS FLOAT[1024]))
        """
        #print(insert_sql)
        conn.execute(insert_sql , (newUID , content_str, add_vector))

#
#
#
def add_embed():
    read_file()
    return

#
#
#
if __name__ == "__main__":
    add_embed()

