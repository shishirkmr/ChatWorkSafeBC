from langchain.schema.retriever import BaseRetriever
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as pinecone_db
from langchain.docstore.document import Document
from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from typing import List

import os
# TODO: API keys to environment variables
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
PINECONE_API_KEY = os.environ['PINECONE_API_KEY']
PINECONE_ENVIRONMENT = "gcp-starter"
PINECONE_INDEX = 'work-safe-bc'


class CustomRetriever(BaseRetriever):

    def _get_relevant_documents(self, prompt: str, run_manager: CallbackManagerForRetrieverRun) -> List[
        Document]:
        """
        _get_relevant_documents is function of BaseRetriever implemented here

        :param query: String value of the query

        """
        num_matches = 4
        embed = OpenAIEmbeddings(
            model='text-embedding-3-small',
            openai_api_key=OPENAI_API_KEY
        )
        pc = pinecone_db(
            api_key=PINECONE_API_KEY
        )
        index = pc.Index(PINECONE_INDEX)

        vectorstore = Pinecone(
            index, embed.embed_query, "text"
        )
        vector_search_results = vectorstore.similarity_search_with_score(
            prompt,
            k=num_matches
        )
        if vector_search_results:
            print('Success Query in Pinecone!!')
            result_docs = []
            for result in vector_search_results:
                print(result)
                if result[1] > 0.59:
                    # Remove low Similarity contents which does not have any Context
                    if result[0].metadata["chunk_size"] > 20:
                        # Remove Small contents which does not have any Context
                        score_percentage = result[1]*100
                        result[0].metadata["score"] = f"{str(round(score_percentage, 2))}%"
                        result_docs.append(result[0])
            print(result_docs)
            return result_docs

class CustomNERRetriever(BaseRetriever):

    def _get_relevant_documents(self, prompt: str, run_manager: CallbackManagerForRetrieverRun) -> List[
        Document]:
        """
        _get_relevant_documents is function of BaseRetriever implemented here

        :param query: String value of the query

        """
        num_matches = 4
        embed = OpenAIEmbeddings(
            model='text-embedding-3-small',
            openai_api_key=OPENAI_API_KEY
        )
        pc = pinecone_db(
            api_key=PINECONE_API_KEY
        )
        index = pc.Index(PINECONE_INDEX)

        vectorstore = Pinecone(
            index, embed.embed_query, "text"
        )
        vector_search_results = vectorstore.similarity_search_with_score(
            prompt,
            k=num_matches
        )
        if vector_search_results:
            print('Success Query in Pinecone!!')
            result_docs = []
            for result in vector_search_results:
                print(result)
                if result[1] > 0.59:
                    # Remove low Similarity contents which does not have any Context
                    if result[0].metadata["chunk_size"] > 20:
                        # Remove Small contents which does not have any Context
                        score_percentage = result[1]*100
                        result[0].metadata["score"] = f"{str(round(score_percentage, 2))}%"
                        result_docs.append(result[0])
            print(result_docs)
            return result_docs