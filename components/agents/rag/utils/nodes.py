from components.agents.rag.utils.state import state as State
from langchain_core.messages.tool import ToolMessage
from prompts.rag_prompts import system_prompt, user_prompt
from objects import llm_client
from components.tools.rag_tool import rag_tools
from logger_ import logger
from langchain_core.messages import HumanMessage
from database.sqlite import insert_token_tracking

llm_with_tools = llm_client.client.bind_tools(tools=rag_tools)
def rag_agent(state:State):
    try:
        logger.info("Starting RAG agent processing")
        user_query = state['user_query']
        logger.debug(f"Received user query: {user_query}")
        
        if(state["messages"].__len__()>0 and isinstance(state["messages"][-1],ToolMessage)):
            logger.info("Processing tool agent response")
            try:
                llm_response = llm_with_tools.invoke(state["messages"])
                logger.info("Successfully generated LLM response after tool call")

                input_token=llm_response.usage_metadata['input_tokens']
                output_token=llm_response.usage_metadata['output_tokens']
                total_tokens=llm_response.usage_metadata['total_tokens']
                insert_token_tracking(user_query, "rag_agent", "rag_agent_node", input_token, output_token, total_tokens)

                return {"messages": [llm_response],"model_output":llm_response.content}
            except Exception as e:
                logger.error(f"Error generating LLM response after tool call: {str(e)}")
                raise e

        logger.info("Generating initial LLM response")
        message=[
            ("system",system_prompt),
            ("user",user_prompt.format(user_query=user_query))
        ]
        
        try:
            response = llm_with_tools.invoke(message)

            input_token=response.usage_metadata['input_tokens']
            output_token=response.usage_metadata['output_tokens']
            total_tokens=response.usage_metadata['total_tokens']
            insert_token_tracking(user_query, "rag_agent", "rag_agent_node", input_token, output_token, total_tokens)

            logger.info("Successfully generated initial LLM response")
            return {"messages":[response]}
        except Exception as e:
            logger.error(f"Error generating initial LLM response: {str(e)}")
            logger.debug(f"System prompt: {system_prompt}")
            logger.debug(f"User prompt: {user_prompt.format(user_query=user_query)}")
            raise e

    except Exception as e:
        logger.error(f"Error in RAG agent: {str(e)}")
        raise e