from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv()
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')


retriever = TavilySearchAPIRetriever(k=3, api_key=TAVILY_API_KEY)

prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

Context: {context}

Question: {question}"""
)

chain = (
    RunnablePassthrough.assign(
        context=(lambda x: x["question"]) | retriever) | prompt
    | ChatOpenAI(model="gpt-3.5-turbo")
    | StrOutputParser()
)

result = chain.invoke({"question": "Tiny SPL是什么？"})
print(result)
