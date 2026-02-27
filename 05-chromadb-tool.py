import chromadb

def list_collections(db_path: str):
    client = chromadb.PersistentClient(path=db_path)
    collections = client.list_collections()
    print(f"chromadb path:{db_path} 有 {len(collections)} 个 collection")
    for index, collection in enumerate(collections):
        print(f"collection {index}: {collection.name}, 共有{collection.count()}条记录")

def delete_collection(db_path: str, collection_name: str):
    client = chromadb.PersistentClient(path=db_path)
    try:
        client.delete_collection(name=collection_name)
        print(f"collection {collection_name} 已删除")
    except Exception as e:
        print(f"删除 collection {collection_name} 失败: {e}")

if __name__ == "__main__":
    db_path = "./chroma_langchain_db"
    list_collections(db_path)
    # delete_collection(db_path, "example_collection")