from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("CLOUDRU_API_KEY"),
    base_url=os.getenv("CLOUDRU_BASE_URL")
)

response = client.chat.completions.create(
    model="Qwen/Qwen3-Coder-Next",
    messages=[
        {
            "role": "user",
            "content": "Напиши одно предложение о том, что такое RAG."
        }
    ],
    temperature=0.3,
    max_tokens=100
)

print(response.choices[0].message.content)
