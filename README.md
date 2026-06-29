# Knowledge Agent

AI-ассистент для поиска информации по корпоративным документам. Загружает `.docx`-файлы, индексирует их в векторную базу и отвечает на вопросы по содержимому через LLM.

Реализован на основе RAG (Retrieval-Augmented Generation): вопрос пользователя преобразуется в embedding, ChromaDB находит наиболее релевантные фрагменты документов, и LLM формирует ответ строго на основе найденного контекста.

## Стек

- **Python 3**
- **Streamlit** — веб-интерфейс
- **ChromaDB** — векторное хранилище
- **Cloud.ru Foundation Models API** — LLM и embeddings
  - `Qwen/Qwen3-Embedding-0.6B` — embeddings
  - `Qwen/Qwen3-Coder-Next` — генерация ответов
- **python-docx** — чтение `.docx`-файлов

## Структура проекта

```
.
├── app.py                  # Streamlit UI
├── requirements.txt
├── data/                   # Исходные документы (.docx)
├── chroma_db/              # Векторная БД (создаётся индексацией)
└── src/
    ├── loader.py           # Загрузка .docx из data/
    ├── chunker.py          # Разбиение текста на чанки
    ├── embedding.py        # Получение embeddings
    ├── vector_store.py     # Индексация документов в ChromaDB
    ├── rag.py              # Поиск + ответ через LLM
    ├── check_db.py         # Проверка состояния коллекции
    └── test_cloudru.py     # Проверка доступа к Cloud.ru API
```

## Установка

```bash
git clone https://github.com/kerakruchi/knowledge-agent.git
cd knowledge-agent

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Настройка

Скопируйте шаблон переменных окружения и заполните своими ключами:

```bash
cp .env.example .env
```

Содержимое `.env`:

```
CLOUDRU_API_KEY=ваш_ключ_от_cloud_ru
CLOUDRU_BASE_URL=https://foundation-models.api.cloud.ru/v1
```

## Использование

**1. Положите документы (`.docx`) в папку `data/`**

**2. Проиндексируйте документы в ChromaDB:**

```bash
python -m src.vector_store
```

**3. Запустите веб-интерфейс:**

```bash
streamlit run app.py
```

Или задайте вопрос из командной строки:

```bash
python -m src.rag
```

## Как это работает

1. `loader.py` читает все `.docx`-файлы из `data/`
2. `chunker.py` режет текст на чанки по 1000 символов с перекрытием 200 символов
3. `embedding.py` отправляет каждый чанк в Cloud.ru и получает вектор
4. `vector_store.py` сохраняет чанки + векторы в локальную ChromaDB
5. При запросе `rag.py` ищет 5 ближайших чанков и передаёт их вместе с вопросом в LLM
6. LLM отвечает строго на основе контекста; если ответа в документах нет — сообщает об этом

## Параметры

В `src/chunker.py`:
- `CHUNK_SIZE = 1000` — размер чанка
- `OVERLAP = 200` — перекрытие между соседними чанками

В `src/rag.py`:
- `n_results=5` — сколько чанков ищется для каждого вопроса
- `temperature=0.2`, `max_tokens=300` — параметры генерации
