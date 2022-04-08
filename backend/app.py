from docarray import DocumentArray, Document
from jina import Flow
from config import DATA_FILE, DATABASE_NAME, TABLE_NAME
import click



# docs = DocumentArray(
    # storage="sqlite", config={"connection": DATABASE_NAME, "table_name": TABLE_NAME}
# )


qa_docs = DocumentArray.from_csv(
    DATA_FILE, field_resolver={"question": "text"}, size=10
)
# docs.extend(qa_docs)

flow = (
    Flow(protocol="http", port=23456)
    .add(
        name="encoder",
        uses="jinahub://TransformerTorchEncoder",
        uses_with={
            "pretrained_model_name_or_path": "sentence-transformers/paraphrase-mpnet-base-v2"
        },
        install_requirements=True,
    )
    .add(uses="jinahub://SimpleIndexer", install_requirements=True)
)


def index():
    # os.remove(DATABASE_NAME)
    with flow:
        flow.index(qa_docs, show_progress=True)


def search(string: str):
    doc = Document(text=string)
    with flow:
        results = flow.search(doc)

    print(results[0].matches)

    for match in results[0].matches:
        print(match.text)

def search_restful():
    with flow:
        flow.block()


index()
search_restful()
