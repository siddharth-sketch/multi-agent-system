from langchain_core.tools import tool
from langchain_openai import AzureOpenAIEmbeddings
import os
from objects import quadrant_client
from objects import embedder
from database.sqlite import insert_token_tracking
from logger_ import logger
from langgraph.prebuilt import ToolNode


@tool
def database_retrival(user_input: str)-> str:
    """ VECTOR database retrival operation """
    try:
        logger.info("Starting database retrieval operation")
        logger.debug(f"Processing user input: {user_input}")

        try:
            emb = embedder.embed_query(user_input)
            logger.debug("Successfully generated embeddings")
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise e

        try:
            search_results = quadrant_client.search(
                collection_name="Etisalat_approach1",
                query_vector=emb,
                limit=1,  
            )
            logger.debug("Successfully performed vector search")
        except Exception as e:
            logger.error(f"Error performing vector search: {str(e)}")
            raise e

        retrieved_text = search_results[0].payload["text"]
        logger.info("Successfully retrieved text from database")
        logger.debug(f"Retrieved text: {retrieved_text}")
        
        return retrieved_text

    except Exception as e:
        logger.error(f"Error in database retrieval operation: {str(e)}")
        raise e

rag_tools=[database_retrival]
tool_node = ToolNode(tools=rag_tools)