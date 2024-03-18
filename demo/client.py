
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langserve import RemoteRunnable
import json


# prompt = [
#     SystemMessage(content='Act like either a cat or a parrot.'),
#     HumanMessage(content='Hello!')
# ]

# # Supports astream
# async for msg in anthropic.astream(prompt):
#     print(msg, end="", flush=True)

# prompt = ChatPromptTemplate.from_messages(
#     [("system", "Tell me a long story about {topic}")]
# )

# # Can define custom chains
# chain = prompt | RunnableMap({
#     "openai": openai,
# })

# chain.batch([{"topic": "parrots"}, {"topic": "cats"}])

def invoke():
    chat = RemoteRunnable("http://localhost:8000/chat/")
    # openai.invoke({"topic": "what is solana"})
    result = chat.invoke({"topic": "what is solana"})
    # print(result['output'])
    print(json.dumps(result))



if __name__ == "__main__":
    invoke()