from src.loader import load_documents

# Размер чанка
CHUNK_SIZE = 1000

# Перекрытие между соседними чанками
OVERLAP = 200


def split_text(text):
    chunks = []

    # Насколько сдвигаемся каждый раз
    step = CHUNK_SIZE - OVERLAP

    for i in range(0, len(text), step):
        chunk = text[i:i + CHUNK_SIZE]

        # Не добавляем пустые чанки
        if chunk.strip():
            chunks.append(chunk)

    return chunks


if __name__ == "__main__":

    documents = load_documents()

    for doc in documents:

        chunks = split_text(doc["text"])

        print(f"\nДокумент: {doc['file_name']}")
        print(f"Количество чанков: {len(chunks)}")

        print("\nПервый чанк:\n")
        print(chunks[0])

        print("\nВторой чанк:\n")
        if len(chunks) > 1:
            print(chunks[1])