import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("knowledge_base")

print("Количество чанков:", collection.count())