# streamlit run main.py     // Для запуска кода

from g4f.client import Client
import streamlit as st
from constants.interface_labels import c_title_page, c_title, c_submit_btn, \
    c_submit_btn_place_holder, \
    c_request_error, c_loader, c_response

# Настройка страницы
st.set_page_config(page_title=c_title_page, layout="wide")


def get_translation(text, model):
    client = Client()
    try:
        response = client.chat.completions.create(
            # model="gpt-4o-mini",
            model=model,
            messages=[
                {"role": "user", "content": text}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"{c_request_error}: {e}"


# Разделение интерфейса
col1, _, col2 = st.columns([4, 6, 2])
container = st.container()
input_text = st.text_area("", height=300, placeholder=c_submit_btn_place_holder)

with col1:
    st.write(f'# {c_title}')
with col2:
    model_selector = st.selectbox(
        '',
        options=["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"],
        index=0,
    )
with container:
    translate_button = st.button(c_submit_btn, disabled=not input_text)

if translate_button:
    with st.spinner(c_loader):
        translation = get_translation(input_text, model_selector)
        st.subheader(c_response)
        st.write(translation)

st.markdown(
    '<div style="font-size: 0.6rem; marginTop: 1em">'
    '<p style="marginBottom: 0">- Сервис не хранит историю запросов</p>'
    '<p style="marginBottom: 0">- Версия gpt-3.5-turbo самая быстрая</p>'
    '<p style="marginBottom: 0">- Если в ответ приходит ошибка, попробуйте</p>'
    '<p style="marginBottom: 0; marginLeft: 0.5em">  добавить несколько восклицательных знаков</p>'
    '<p style="marginBottom: 0; marginLeft: 0.5em">  в конец текстак или поменять версию gpt</p>'
    '</div>',
    unsafe_allow_html=True
)
