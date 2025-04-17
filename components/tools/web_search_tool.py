from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from objects import search
from logger_ import logger

@tool
def web_tool(user_input: str):
    '''Web search tool for etisalat.ae domain'''
    try:
        logger.info("Starting web search tool execution")
        logger.debug(f"Processing user input: {user_input}")

        try:
            # Perform the search
            results = search.invoke(f"site:etisalat.ae {user_input}")
            logger.debug(f"Search results received: {results}")
        except Exception as e:
            logger.error(f"Error performing search: {str(e)}")
            raise e

        try:
            # Format the results
            formatted_results = {
                "search_query": user_input,
                "results": []
            }
            for i, result in enumerate(results, 1):
                formatted_results["results"].append({
                    "id": i,
                    "title": result["title"],
                    "url": result["url"],
                    "content": result["content"][:200]
                })
            logger.debug(f"Formatted results: {formatted_results}")
        except Exception as e:
            logger.error(f"Error formatting results: {str(e)}")
            raise e

        logger.info("Web search tool execution completed successfully")
        return formatted_results

    except Exception as e:
        logger.error(f"Error in web search tool: {str(e)}")
        return f"An error occurred: {str(e)}"

web_tools=[web_tool]
tool_node = ToolNode(tools=web_tools)