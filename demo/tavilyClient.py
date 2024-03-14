from dotenv import load_dotenv
load_dotenv()
import os
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

# from langchain_community.retrievers import TavilySearchAPIRetriever

# retriever = TavilySearchAPIRetriever(k=3, api_key=TAVILY_API_KEY)

# retriever.invoke("what is cNFT?")


from tavily import TavilyClient
tavily = TavilyClient(api_key=TAVILY_API_KEY)
# For basic search:
result = tavily.search(query="what is cNFT?")
print(result)
# For advanced search:
# tavily.search(query="Should I invest in Apple right now?", search_depth="advanced")