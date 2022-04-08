import streamlit as st
from jina import Client
from docarray import Document
from config import PORT, TOP_K, SERVER
from streamlit_chat import message


def search_by_text(input, server=SERVER, port=PORT, limit=TOP_K):
    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        Document(text=input),
        parameters={"limit": limit},
        return_results=True,
        show_progress=True,
    )
    matches = response[0].matches

    return matches

st.set_page_config(
    page_title="Jina Chatbot",
    page_icon=":robot:"
)

st.title("COVID-19 Chatbot")
message_area = st.container()

question = st.text_input(label="Question")
search_button = st.button(label="Search")


if search_button:
    matches = search_by_text(question)
    for match in matches:
        with message_area:
            message(question, is_user=True)
            message(f"""
{match.tags['title']}
{match.tags['answer']}
                """)
