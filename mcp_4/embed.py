from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import os
import ollama
import random
import uuid
import glob
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

COLLE_NAME="my_document"
# .envファイルから環境変数を読み込む
load_dotenv()

folder_path = "./data"
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

    clientQdrant = QdrantClient(
        url="http://localhost:6333"
    )
    #
    for i, d in enumerate(data):
        print(f"data:{str(i)} \n")
        content_str = d["content"]
        print(f"{content_str}\n")
        response = ollama.embeddings(model="qwen3-embedding:0.6b", prompt=content_str)
        embedding = response["embedding"]
        print("embedding.len=" + str(len(embedding)) )
        add_vector = embedding

        newUid = uuid.uuid4()
        points = [
            PointStruct(
                id=newUid,
                vector=add_vector,
                payload={
                    "content": content_str,
                    "category": "none"
                }
            )
        ]
        clientQdrant.upsert(
            collection_name=COLLE_NAME,
            points=points
        )            


#
#
#
if __name__ == "__main__":
    print("#start")
    read_file()

