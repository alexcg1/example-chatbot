from docarray import DocumentArray, Document
from jina import Flow
from config import DATA_FILE, DATABASE_NAME, TABLE_NAME
import os

docs = DocumentArray(
    storage="sqlite", config={"connection": DATABASE_NAME, "table_name": TABLE_NAME}
)


qa_docs = DocumentArray.from_csv(
    DATA_FILE, field_resolver={"question": "text"}, size=10
)
docs.extend(qa_docs)

flow = Flow().add(
    name="encoder",
    uses="jinahub://TransformerTorchEncoder",
    uses_with={"pretrained_model_name_or_path": "sentence-transformers/paraphrase-mpnet-base-v2"},
    install_requirements=True,
)

def index():
    # os.remove(DATABASE_NAME)
    with flow:
        indexed_docs = flow.index(docs, show_progress=True)

    indexed_docs.summary()

def search(string: str):
    doc = Document(text=string)
    with flow:
        results = flow.search(doc)

    print(results[0].matches)

index()
search("pets")
