from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain.utils import get_from_dict_or_env
from pydantic.v1 import BaseModel, Extra, root_validator

from .doc_prompts import (
    Modes,
    SEARCH
)
from langchain.utils import get_from_dict_or_env


class DocApiWrapper(BaseModel):
    """ Wrapper for searching documents. """
    connection_string: str
    embeddings: OpenAIEmbeddings
    collection_name: str = "documents"
    operations: list[dict] = [
        {
            "mode": Modes.SEARCH,
            "name": "Search documents",
            "description": SEARCH,
        }
    ]

    class Config:
        """ Configuration for this pydantic object. """
        extra = Extra.forbid
        arbitrary_types_allowed = True

    def list_operations(self) -> list[dict]:
        return self.operations

    @root_validator(pre=True)
    def validate_env(cls, data: dict) -> dict:
        driver = get_from_dict_or_env(
            data, "db_driver", "DB_DRIVER", "psycopg")
        host = get_from_dict_or_env(data, "db_host", "DB_HOST")
        port = get_from_dict_or_env(data, "db_port", "DB_PORT")
        database = get_from_dict_or_env(data, "db_database", "DB_DATABASE")
        user = get_from_dict_or_env(data, "db_user", "DB_USER")
        password = get_from_dict_or_env(data, "db_password", "DB_PASSWORD")

        connection_string = PGVector.connection_string_from_db_params(
            driver=driver,
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        data["connection_string"] = connection_string

        openai_embeddings = OpenAIEmbeddings()
        data["embeddings"] = openai_embeddings

        return data

    def run(self, mode: str, text: str | None) -> str:
        """ Based on the mode from the caller, run the appropriate function. """
        if mode == Modes.SEARCH:
            return self.search_docs(text)
        else:
            raise ValueError(f"Got unexpected mode {mode}")

    def load_docs(self, path: str) -> None:
        """ Loads a text file and stores it in the database. """

        loader = TextLoader(path, encoding="utf-8")
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        split_docs = text_splitter.split_documents(documents)

        PGVector.from_documents(
            connection_string=self.connection_string,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            documents=split_docs,
        )

    def search_docs(self, query: str) -> list[str]:
        """ Searches the database for the given query. """
        store = PGVector(
            connection_string=self.connection_string,
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
            distance_strategy=DistanceStrategy.COSINE,
        )

        retriever = store.as_retriever(
            search_kwargs={"k": 3, "score_threshold": "0.8"})
        result_docs = retriever.get_relevant_documents(query=query)
        if result_docs is None or len(result_docs) == 0:
            return []

        return [doc.page_content for doc in result_docs]
