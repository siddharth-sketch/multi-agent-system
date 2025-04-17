# we will have three nodes in the supervisor agent
# 1. text2sql agent
# 2. rag agent
# 3. web search agent

# Each agent will contain compiled graph object of each.


from components.agents.text2sql.text2sql_Agent_flow import app_text_2_sql
from components.agents.supervisor.utils.sup_state import State
from components.agents.text2sql.utils.state import State as Text2SqlState  
from components.agents.rag.rag_workflow import app_rag_agent 
from components.agents.web_search_agent.web_search_agent_flow import app_web_agent 
from components.agents.misleading_agent.misleading_agent_flow import app_misleading_agent
from objects import llm_client
from prompts.text2sql_prompts import supervisor_system_prompt,supervisor_user_prompt  
import json
from langchain_core.messages import HumanMessage
from logger_ import logger
from database.sqlite import insert_token_tracking

def supervisor_agent(state: State):
    '''
    This is the supervisor agent which will be used to select the right agent to handle the user's query.
    '''
    try:
        logger.info(f"------------------------------NEW USER QUERY------------------------------: {state['user_query']}")
        user_question=HumanMessage(content=state['user_query'])

        if(state['user_query']=="get_history"):
            return {
                "messages": state['messages']
            }
        logger.info("Starting supervisor agent processing")
        user_query = state["user_query"]
        logger.debug(f"Processing user query: {user_query}")

        response=llm_client.infer(system_prompt=supervisor_system_prompt,user_prompt=supervisor_user_prompt.format(user_query=user_query))

        input_token=response.usage_metadata['input_tokens']
        output_token=response.usage_metadata['output_tokens']
        total_tokens=response.usage_metadata['total_tokens']
        insert_token_tracking(user_query, "supervisor_agent", "supervisor_agent_node", input_token, output_token, total_tokens)
        
        response_json = json.loads(response.content)
        agent_name = response_json["agent_name"]
        logger.info(f"Selected agent: {agent_name}")

        return {
            "agent_name": agent_name,
            "messages": [user_question]+[response]
        }
    except Exception as e:
        logger.error(f"Error in supervisor agent: {str(e)}")
        raise e


def text2sql_agent(state: State):
    try:
        logger.info("Starting text2sql agent processing")
        user_query = state["user_query"]
        logger.debug(f"Processing user query: {user_query}")

        config = {"configurable": {"thread_id": "1"}}
        logger.debug(f"Using config: {config}")

        text2sql_output = app_text_2_sql.invoke({"user_query": user_query}, config)
        logger.info("Successfully processed text2sql request")

        return {
            "agent_name": "text2sql",
            "messages": text2sql_output["messages"],
            "agent_output": text2sql_output["model_output"]
        }
    except Exception as e:
        logger.error(f"Error in text2sql agent: {str(e)}")
        raise e


def rag_agent(state: State):
    try:
        logger.info("Starting RAG agent processing")
        user_query = state["user_query"]
        logger.debug(f"Processing user query: {user_query}")

        config = {"configurable": {"thread_id": "1"}}
        logger.debug(f"Using config: {config}")

        rag_output = app_rag_agent.invoke({"user_query": user_query}, config)
        logger.info("Successfully processed RAG request")
        return {
            "agent_name": "rag",
            "messages": rag_output["messages"],
            "agent_output": rag_output["model_output"]
        }
    except Exception as e:
        logger.error(f"Error in RAG agent: {str(e)}")
        raise e


def web_search_agent(state: State):
    try:
        logger.info("Starting web search agent processing")
        user_query = state["user_query"]
        logger.debug(f"Processing user query: {user_query}")

        config = {"configurable": {"thread_id": "1"}}
        logger.debug(f"Using config: {config}")

        web_search_output = app_web_agent.invoke({"user_query": user_query}, config)
        logger.info("Successfully processed web search request")

        return {
            "agent_name": "web_search",
            "messages": web_search_output["messages"],
            "agent_output": web_search_output["model_output"]
        }
    except Exception as e:
        logger.error(f"Error in web search agent: {str(e)}")
        raise e


def misleading_agent(state: State):
    try:
        logger.info("Starting misleading agent processing")
        user_query = state["user_query"]
        logger.debug(f"Processing user query: {user_query}")

        config = {"configurable": {"thread_id": "1"}}
        logger.debug(f"Using config: {config}")

        misleading_output = app_misleading_agent.invoke({"user_query": user_query}, config)
        logger.info("Successfully processed misleading request")

        return {
            "agent_name": "misleading",
            "messages": misleading_output['messages'],
            "agent_output": misleading_output['model_output']
        }
    except Exception as e:
        logger.error(f"Error in misleading agent : {str(e)}")
