from langchain.agents import tool
from langchain_openai import ChatOpenAI
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage

from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0)


@tool
def get_balance(address: str) -> str:
    """Returns the sol balance of an address."""
    return "0.1 sol"


MEMORY_KEY = "chat_history"
chat_history = []

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant",
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [get_balance]
llm_with_tools = llm.bind_tools(tools)


agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# print(list(agent_executor.stream({"input": "How many letters in the word eudca"})))

# print(llm.invoke("How many letters in the word educa"))

input1 = "what is solana?"
result = agent_executor.invoke({"input": input1, "chat_history": chat_history})
chat_history.extend(
    [
        HumanMessage(content=input1),
        AIMessage(content=result["output"]),
    ]
)
result2 = agent_executor.invoke({"input": "sol balance of GSSZb19uq1UKDuWBxsUF5VEbWGEo7NMuBqfeHtyFCp93", "chat_history": chat_history})

print(result["output"])
print(result2["output"])