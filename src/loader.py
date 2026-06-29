import os
from docx import Document

DATA_DIR = "data"


def load_documents():

    documents = []

    for file_name in os.listdir(DATA_DIR):

        if not file_name.endswith(".docx"):
            continue

        file_path = os.path.join(DATA_DIR, file_name)

        doc = Document(file_path)

        text = ""

        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        documents.append(
            {
                "file_name": file_name,
                "text": text
            }
        )

    return documents


if __name__ == "__main__":

    docs = load_documents()

    print(f"Найдено документов: {len(docs)}\n")

    for doc in docs:

        print("=" * 50)
        print(doc["file_name"])
        print("=" * 50)

        print(doc["text"][:300])
        print()