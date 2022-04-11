# Jina + Streamlit Chatbot

This simple example adapts [Jina Hello Chatbot](https://docs.jina.ai/get-started/hello-world/covid-19-chatbot/) in the following ways:

- Use [Jina Hub](https://hub.jina.ai) Executors
- Use [Streamlit](https://streamlit.io/) front-end (with the awesome [Streamlit chat](https://github.com/AI-Yash/st-chat) library)
- Easy deployment with Docker-Compose

## Run

### Backend

1. `cd backend`
2. `python app.py`

### Frontend

1. `cd frontend`
2. `python frontend.py`

## Deploy

`docker-compose up`

## Limitations

This is still a WIP, so right now:

- No dataset getter
- All data is indexed at start
- Only a subset of data is indexed to keep it quick

All of these are relatively simple to fix
