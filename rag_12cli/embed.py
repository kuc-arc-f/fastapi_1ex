import os
import random
import uuid
import glob
import weaviate
from google import genai
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from weaviate.connect import ConnectionParams
from weaviate.classes.config import Property, DataType
import weaviate.classes.config as Configure

COLLECT_NAME = "document"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
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
clientWeaviate = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_url(
        "http://localhost:8080",
        grpc_port=50051
    )
)


#
#
#
def read_file():
    client = genai.Client(api_key=GOOGLE_API_KEY)
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

    clientWeaviate.connect()
    # 接続確認
    print(clientWeaviate.is_ready())

    if not clientWeaviate.collections.exists(COLLECT_NAME):
        clientWeaviate.close()
        print("not-exeist-COLLECT"+ COLLECT_NAME)
        return

    for i, d in enumerate(data):
        print(f"data:{str(i)} \n")
        content_str = d["content"]
        print(f"{content_str}\n")
        client = genai.Client(api_key=GOOGLE_API_KEY)
        result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=content_str)

        #print(f"次元数: {len(embedding)}")        
        if len(result.embeddings) > 0:
            print("len="+ str(len(result.embeddings))) 
            embedding = result.embeddings[0]
            newUid = uuid.uuid4()
            #collections
            collection = clientWeaviate.collections.get(COLLECT_NAME)
            collection.data.insert(
                properties={
                    "content": content_str,
                    "category": "none"
                },
                vector=embedding.values  # embedding
            )

    #close
    clientWeaviate.close()

#
#
#
if __name__ == "__main__":
    print("#start")
    read_file()

