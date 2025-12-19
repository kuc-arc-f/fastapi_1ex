import chromadb
import os
import uuid
import glob
from google import genai
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# .envファイルから環境変数を読み込む
load_dotenv()

folder_path = "./data"
collection_name = "my_document_collection"
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
def read_file(collection):
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

    #
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
            collection.add(
                ids=[str(uuid.uuid4())],
                embeddings=[embedding.values],
                documents=[content_str]
            )

#
#
#
def add_embed():
   # クライアントの初期化 (ローカルにデータベースファイルを作成)
    # インメモリで実行する場合は chromadb.Client() を使用します
    client = chromadb.PersistentClient(path="./my_chroma_db") 
    print("ChromaDB クライアントを初期化しました。")

    # コレクションの作成または取得
    # get_or_create を使うと、既に存在すればそれを取得し、なければ新しく作成します
    collection = client.get_or_create_collection(name=collection_name)

    print(f"コレクション '{collection_name}' を作成/取得しました。")
    read_file(collection)
    return

#
#
#
if __name__ == "__main__":
    add_embed()

