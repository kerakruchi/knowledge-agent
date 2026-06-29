import streamlit as st
from src.rag import ask

st.set_page_config(
    page_title="Knowledge Agent",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Knowledge Agent")
st.write("AI-ассистент для поиска информации по корпоративным документам")

question = st.text_input(
    "Введите вопрос",
    placeholder="Например: Когда начинается рабочий день?"
)

if st.button("Получить ответ"):

    if not question.strip():
        st.warning("Введите вопрос.")
    else:

        with st.spinner("Ищу информацию в базе знаний..."):

            try:
                answer, sources = ask(question)

                st.success("Ответ")

                st.write(answer)

                st.divider()

                st.subheader("Источники")

                for source in sources:
                    st.write(f"📄 {source}")

            except Exception as e:
                st.error(f"Ошибка: {e}")