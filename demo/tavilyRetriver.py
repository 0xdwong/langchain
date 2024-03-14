from dotenv import load_dotenv
load_dotenv()
import os
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

from typing import List
from langchain_core.documents import Document
from langchain_community.retrievers import TavilySearchAPIRetriever
retriever = TavilySearchAPIRetriever(k=3,api_key=TAVILY_API_KEY)


def retrieve(question: str) -> List[Document]:
    result = retriever.invoke(question)
    print(result)
    return result

retrieve("what year was breath of the wild released?")