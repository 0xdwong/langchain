#!/usr/bin/env python
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv
load_dotenv()


# 1. Load Retriever
loader = WebBaseLoader("https://www.helius.dev/blog/the-solana-programming-model-an-introduction-to-developing-on-solana")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
vector_db = Chroma.from_documents(documents, OpenAIEmbeddings())
retriever = vector_db.as_retriever()


# 2. Create webRetriever
retriever_tool = create_retriever_tool(
    retriever,
    "langsmith_search",
    "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)
search = TavilySearchResults()

# 3. Create Tools
# tools = [retriever_tool]
# tools = [search]
tools = [retriever_tool,search]




# 4. Create Agent
prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


result = agent_executor.invoke({"input": '介绍下 solana rent', "chat_history": []})
print("========" + result["output"])