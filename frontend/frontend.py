from jina import Client
from config import SERVER, PORT, TOP_K
from docarray import Document
import streamlit as st
from streamlit_chat import message

st.set_page_config(page_title="Jina COVID-19 Chatbot", page_icon=":robot:")

st.header("🤖 Jina COVID-19 Chatbot")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

st.sidebar.markdown("# Introduction\n\nThis chatbot is built using: \n\n - [**DocArray**](https://docarray.jina.ai): The data structure for unstructured data\n- [**Jina**](https://github.com/jina-ai/jina/): Cloud native neural search framework\n- [**Streamlit**](https://streamlit.io/) - frontend\n- [**Streamlit-chat**](https://github.com/AI-Yash/st-chat): Chat plugin for Streamlit\n\n## Useful links\n\n- [Code repository](https://github.com/alexcg1/example-chatbot)\n - [COVID-QA dataset from Kaggle](https://www.kaggle.com/xhlulu/covidqa/)\n - [Jina Hello Chatbot](https://docs.jina.ai/get-started/hello-world/covid-19-chatbot/) (the basis for this example)\n\n## Disclaimer\n\nThis chatbot is intended only as a technical demonstration. **DO NOT TAKE MEDICAL ADVICE FROM STRANGE BOTS ON THE INTERNET** (especially ones with outdated datasets)")


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
