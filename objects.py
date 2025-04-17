from adapter.ai_adapter.openai_adapter import AzureopenAi_
from adapter.database_adapter.sqlite_adapter import sqlite
from qdrant_client import QdrantClient
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()
memory = MemorySaver()
quadrant_client  = QdrantClient(
    url="https://408d4eee-81fe-427f-a8cb-128923dc1053.us-east4-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.oipZao46XuR3g0FD7uj70JwPTU-AOxv6aJWBStqy9DQ",
) 
search = TavilySearchResults(max_results=3)
llm_client = AzureopenAi_("gpt-4o")
sqlite_client = sqlite("etisalat_sales.db")

embedder = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-ada-002",  
    azure_endpoint=os.getenv('emb_endpoint'), 
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),  
    api_version=os.getenv("OPENAI_API_VERSION") 
)


