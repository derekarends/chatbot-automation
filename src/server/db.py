from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain.docstore.document import Document
from langchain.utils import get_from_dict_or_env
from langchain.vectorstores.base import VectorStoreRetriever
from pydantic.v1 import BaseModel, root_validator


class PgVector(BaseModel):
    connection_string: str
    embeddings: OpenAIEmbeddings

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

    def load(self, path: str, collection_name: str) -> None:
        """ Loads a text file and stores it in the database. """

        loader = TextLoader(path)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        PGVector.from_documents(
            connection_string=self.connection_string,
            embedding=self.embeddings,
            documents=docs,
            collection_name=collection_name,
        )

    def search(self, query: str, collection_name: str) -> list[str]:
        """ Searches the database for the given query. """

        store = PGVector(
            connection_string=self.connection_string,
            embedding_function=self.embeddings,
            collection_name=collection_name,
            distance_strategy=DistanceStrategy.COSINE
        )

        retriever = store.as_retriever(
            search_kwargs={"k": 3, "score_threshold": "0.8"})
        docs = retriever.get_relevant_documents(query=query)
        if docs is None or len(docs) == 0:
            return []

        return [doc.page_content for doc in docs]
