from dotenv import load_dotenv
from openai import OpenAI
import os
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv("CLOUDRU_API_KEY"),
    base_url=os.getenv("CLOUDRU_BASE_URL"),
    timeout=120
)


def get_embedding(text):
    """
    Возвращает embedding для переданного текста.
    При временной ошибке делает до 3 попыток.
    """

    for attempt in range(3):

        try:

            response = client.embeddings.create(
                model="Qwen/Qwen3-Embedding-0.6B",
                input=text
            )

            return response.data[0].embedding

        except Exception as e:

            print(f"Попытка {attempt + 1}/3 не удалась")

            if attempt == 2:
                raise e

            time.sleep(2)


if __name__ == "__main__":

    embedding = get_embedding(
        "Компания предоставляет сотрудникам ежегодный отпуск."
    )

    print(f"Размер embedding: {len(embedding)}")
    print(embedding[:10])