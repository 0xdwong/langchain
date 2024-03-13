from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)


# result = llm.invoke("how can langsmith help with testing?")
# print(result.content)


# prompt 模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

chain = prompt | llm 
result = chain.invoke({"input": "how can langsmith help with testing?"})
print(result.content)