from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

# 加载要索引的数据
loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
docs = loader.load()

# 嵌入模型
embeddings = OpenAIEmbeddings()


# 将数据索引到向量存储中
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)


# 建立一个链条，它接收问题和检索到的文档，并生成答案。
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)


# 检索并生成答案
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke(
    {"input": "how can langsmith help with testing?"})
print(response["answer"])
