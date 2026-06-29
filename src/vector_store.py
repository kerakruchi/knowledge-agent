import chromadb

from src.loader import load_documents
from src.chunker import split_text
from src.embedding import get_embedding


# Подключаемся к ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

# Если коллекция уже существует — удаляем ее
try:
    client.delete_collection("knowledge_base")
    print("Старая коллекция удалена.")
except Exception:
    print("Создаем новую коллекцию.")

# Создаем новую коллекцию
collection = client.get_or_create_collection(
    name="knowledge_base"
)

# Загружаем документы
documents = load_documents()

total_chunks = 0

for document in documents:

    print(f"\nОбработка документа: {document['file_name']}")

    chunks = split_text(document["text"])

    print(f"Найдено чанков: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        print(f"   → Обрабатывается чанк {i + 1}/{len(chunks)}")

        embedding = get_embedding(chunk)

        collection.add(
            ids=[f"{document['file_name']}_{i}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "source": document["file_name"]
                }
            ]
        )

        total_chunks += 1

print("\n==============================")
print("Индексация завершена!")
print(f"Всего добавлено чанков: {total_chunks}")
print("==============================")