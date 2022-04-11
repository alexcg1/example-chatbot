from docarray import DocumentArray, Document
from jina import Flow
from config import DATA_FILE, NUM_DOCS, PORT
import click



flow = (
    Flow(protocol="http", port=PORT)
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


def index(num_docs=NUM_DOCS):
    qa_docs = DocumentArray.from_csv(
        DATA_FILE, field_resolver={"question": "text"}, size=num_docs
    )
    with flow:
        flow.index(qa_docs, show_progress=True)


def search_grpc(string: str):
    doc = Document(text=string)
    with flow:
        results = flow.search(doc)

    print(results[0].matches)

    for match in results[0].matches:
        print(match.text)


def search():
    with flow:
        flow.block()


@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=NUM_DOCS)
def main(task: str, num_docs):
    if task == "index":
        index(num_docs=num_docs)
    elif task == "search":
        search()
    else:
        print("Please add '-t index' or '-t search' to your command")


if __name__ == "__main__":
    main()
