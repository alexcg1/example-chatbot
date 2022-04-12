from jina import Client
from config import SERVER, PORT, TOP_K
from docarray import Document
import streamlit as st
from streamlit_chat import message

st.set_page_config(page_title="Jina Chat Bot", page_icon=":robot:")

st.header("Jina Chatbot")
st.markdown("[Github](https://github.com/ai-yash/st-chat)")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def query(payload):
    return search_by_text(payload["inputs"]["text"])


def search_by_text(input, server=SERVER, port=PORT, limit=TOP_K):
    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        Document(text=input),
        parameters={"limit": limit},
        return_results=True,
        show_progress=True,
    )
    match = response[0].matches[0].tags["answer"]

    return match


user_input = st.text_input("What's your question?", "", key="input")

if user_input:
    output = {}
    output["generated_text"] = query(
        {
            "inputs": {
                "past_user_inputs": st.session_state.past,
                "generated_responses": st.session_state.generated,
                "text": user_input,
            },
            "parameters": {"repetition_penalty": 1.33},
        }
    )

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output["generated_text"])

message_container = st.container()
if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        with message_container:
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i], key=str(i))
