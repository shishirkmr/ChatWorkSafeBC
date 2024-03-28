import os

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone as pinecone_db

from custom_retriever import CustomRetriever

# TODO: API keys to environment variables
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
PINECONE_API_KEY = os.environ['PINECONE_API_KEY']
PINECONE_ENVIRONMENT = "gcp-starter"
PINECONE_INDEX = 'work-safe-bc'

PROMPT_CHAT_TEMPLATE = (
    "You are an artificial assistant called ChatWorkSafeBC, and you were designed by Shishir Kumar and trained by researchers from WorkSafeBC."
    "The Workers' Compensation Board of British Columbia, operating as WorkSafeBC, is a statutory agency that came into existence in 1917, after the provincial legislature put into force legislation passed in 1902. This legislation is known as the Workers Compensation Act."
    "WorkSafeBC's mandate includes prevention of occupational injury and occupational disease, which WorkSafeBC accomplishes through education, consultation, and enforcement. It carries out workplace inspections and investigates serious incidents, such as fatalities. The Workers Compensation Act assigns the authority to make the Occupational Health and Safety Regulation of British Columbia."
    "If asked about who you are, do not respond with AI."
    "Answer in a way that is easy to understand."
    "Do not say \"Based on the information you provided, ...\" or \"I think the answer is...\". Just answer the question directly in detail."
    "You are known as ChatWorkSafeBC, built by WorkSafeBC."
)

PROMPT_CHAT_TEMPLATE += """
The below is a conversation between a human and ChatWorkSafeBC, an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
You must respond the human as AI in the output. Remember, just answer the Human question as AI, do not talk as Human.
Make sure to consider the following context in your response:

'''
{context}
'''

Chat History:
{chat_history}

Human: {question}
AI:"""

CHAT_HISTORY = []


class RagChatApplication(object):
    def __init__(self, user_query: str):
        self.user_query = user_query

    def get_chat_history(self):
        # TODO Get Chat History from external Database
        return CHAT_HISTORY

    def generate(self):
        llm = ChatOpenAI(
            temperature=0.7,
            max_tokens=4000,
            model_name="gpt-3.5-turbo-16k"
        )
        window_memory = ConversationBufferWindowMemory(
            llm=llm,
            memory_key="chat_history",
            return_messages=True,
            max_token_limit=300,
            input_key="question",
            output_key="answer"
        )
        for item in CHAT_HISTORY:
            window_memory.save_context({"question": item[0]}, {"answer": item[1]})

        PROMPT_CHAT_TEMPLATE_LANGCHAIN = PromptTemplate(
            template=PROMPT_CHAT_TEMPLATE,
            input_variables=["context", "chat_history", "question"]
        )
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
        custom_retriever = CustomRetriever()
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            # retriever=vectorstore.as_retriever(),
            retriever=custom_retriever,
            memory=window_memory,
            verbose=True,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": PROMPT_CHAT_TEMPLATE_LANGCHAIN},
            get_chat_history=lambda h: h
        )
        #  Get Chat History
        chat_history = self.get_chat_history()

        result = self.chain({"question": self.user_query, "chat_history": chat_history})
        generated_text = result["answer"]
        CHAT_HISTORY.append((str(self.user_query), str(result["answer"])))
        if len(CHAT_HISTORY) > 10:
            CHAT_HISTORY = CHAT_HISTORY[-9:]
        file_names = set()
        links = set()
        scores = []
        for item in result['source_documents']:
            temp_len = len(file_names)
            file_names.add(item.metadata["file_name"])
            links.add(item.metadata["source"])
            if temp_len == len(file_names):
                print(scores)
            else:
                scores.append(item.metadata["score"])
        links = list(links)
        file_names = list(file_names)
        tags = ""
        for link, file_name, score in zip(links, file_names, scores):
            tags += f"""<a href='{link}' target="_blank">Source Link to file {file_name} with Confidence score: {score}</a><br/>"""
        formatted_result = f""" ***Answer*** - {result["answer"]} <br>
                {tags}
        """

        return formatted_result


if __name__ == '__main__':
    rag_chat = RagChatApplication(user_query="What are the Obligations relating to the use of resource roads?")
    # rag_chat = RagChatApplication(user_query="Hi")
    chat_response = rag_chat.generate()
    print(chat_response)
