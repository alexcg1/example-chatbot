FROM jinaai/jina:3.2.10-py39-standard

COPY . /workspace
WORKDIR /workspace

RUN pip install streamlit==1.5.0

EXPOSE 8600

ENTRYPOINT ["streamlit", "run"]
CMD ["frontend.py"]
