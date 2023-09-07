import os
from typing import List, Tuple
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain.docstore.document import Document
from langchain.utils import get_from_dict_or_env
from langchain.vectorstores.base import VectorStoreRetriever
from pydantic import BaseModel, root_validator


class PgVector(BaseModel):
    _retriever: VectorStoreRetriever
    _embeddings: OpenAIEmbeddings
    _connection_string: str

    collection_name: str

    @root_validator()
    def validate_environment(cls, values: dict) -> dict:
        driver = get_from_dict_or_env(
            values, "db_driver", "DB_DRIVER", "psycopg")
        host = get_from_dict_or_env(values, "db_host", "DB_HOST")
        port = get_from_dict_or_env(values, "db_port", "DB_PORT")
        database = get_from_dict_or_env(values, "db_database", "DB_DATABASE")
        user = get_from_dict_or_env(values, "db_user", "DB_USER")
        password = get_from_dict_or_env(values, "db_password", "DB_PASSWORD")

        connection_string = PGVector.connection_string_from_db_params(
            driver=driver,
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        values["_connection_string"] = connection_string

        embeddings = OpenAIEmbeddings()
        values["_embeddings"] = embeddings

        store = PGVector(
            connection_string=connection_string,
            embedding_function=embeddings,
            collection_name='state_of_the_union',
            distance_strategy=DistanceStrategy.COSINE
        )

        retriever = store.as_retriever(search_kwargs={"k": 1})
        values["_retriever"] = retriever

        return values

    def load(self, path: str, collection_name: str) -> None:
        """ Loads a text file and stores it in the database. """

        loader = TextLoader(path)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        PGVector.from_documents(
            embedding=self._embeddings,
            documents=docs,
            collection_name=collection_name,
            connection_string=self._connection_string,
        )

    def search(self, query: str) -> List[Document]:
        """ Searches the database for the given query. """

        docs_with_score = self._retriever.get_relevant_documents(query=query)
        for doc, score in docs_with_score:
            print("-" * 80)
            print("Score: ", score)
            print(doc.page_content)
            print(doc.metadata)
            print("-" * 80)

        return docs_with_score
