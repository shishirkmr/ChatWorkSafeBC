from langchain.vectorstores import Pinecone
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains import RetrievalQA
from langchain.chains import RetrievalQAWithSourcesChain
from pinecone import Pinecone as pinecone_db

import os
# TODO: API keys to environment variables
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
PINECONE_API_KEY = os.environ['PINECONE_API_KEY']
PINECONE_ENVIRONMENT = "gcp-starter"
PINECONE_INDEX = 'work-safe-bc'


class QuestionAnsweringSystem(object):
    def __init__(self, user_query: str):
        self.user_query = user_query

    def generate(self):
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

        # chat completion llm
        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name='gpt-3.5-turbo',
            temperature=0.3
        )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )
        qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
            llm=llm,
            chain_type="stuff",
            return_source_documents=True,
            retriever=vectorstore.as_retriever()
        )

        result = qa_with_sources.invoke(self.user_query)
        link = f"""<a href='{result["sources"]}' target="_blank">Source Link </a>""" if 'sources' in result else ''
        formatted_result = f""" ***Answer*** - {result["answer"]} <br>
        {link}
        """
        # ***Reference Links:*** { ','.join({doc.metadata['source'] for doc in result["source_documents"]}) }
        # ***Source Text:*** {'---------'.join({doc.page_content for doc in result["source_documents"]}) }
        if result["sources"]:
            print(formatted_result)
            return formatted_result
        else:
            print(result["answer"])
            return result["answer"]


if __name__ == '__main__':
    qa = QuestionAnsweringSystem(user_query="What are the Obligations relating to the use of resource roads?")
    # qa = QuestionAnsweringSystem(user_query="Hi")
    qa.generate()
