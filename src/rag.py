import os
import chromadb

from dotenv import load_dotenv
from openai import OpenAI

from src.embedding import get_embedding

load_dotenv()

# Подключаем LLM
llm = OpenAI(
    api_key=os.getenv("CLOUDRU_API_KEY"),
    base_url=os.getenv("CLOUDRU_BASE_URL"),
    timeout=60
)

# Подключаем ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("knowledge_base")


def ask(question):

    # Строим embedding вопроса
    question_embedding = get_embedding(question)

    # Ищем похожие чанки
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(documents)

    response = llm.chat.completions.create(
        model="Qwen/Qwen3-Coder-Next",
        messages=[
            {
                "role": "system",
                "content": """
Ты корпоративный AI-помощник.

Отвечай ТОЛЬКО на основе предоставленного контекста.

Если ответа в документах нет —
напиши:

"Информация в базе знаний отсутствует."

Не придумывай факты.
"""
            },
            {
                "role": "user",
                "content": f"""
Контекст:

{context}

Вопрос:

{question}
"""
            }
        ],
        temperature=0.2,
        max_tokens=300
    )

    answer = response.choices[0].message.content

    sources = []

    for meta in metadatas:
        if meta["source"] not in sources:
            sources.append(meta["source"])

    return answer, sources


if __name__ == "__main__":

    question = input("Введите вопрос: ")

    answer, sources = ask(question)

    print("\n========================")
    print("Ответ")
    print("========================\n")

    print(answer)

    print("\n========================")
    print("Источники")
    print("========================")

    for source in sources:
        print(f"• {source}")