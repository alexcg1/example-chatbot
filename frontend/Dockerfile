FROM jinaai/jina:3.2.10-py39-standard

COPY . /workspace
WORKDIR /workspace

RUN pip install -r docker-requirements.txt

EXPOSE 8600

ENTRYPOINT ["streamlit", "run"]
CMD ["frontend.py"]
