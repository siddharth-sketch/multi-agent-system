from components.agents.misleading_agent.utils.state import State
from objects import llm_client
from prompts.misleading_agent_prompts import misleading_agent_system_prompt,misleading_agent_user_prompt
from logger_ import logger
from database.sqlite import insert_token_tracking

def misleading_agent(state: State):
    try:
        logger.info("Starting misleading agent processing")
        user_query = state["user_query"]
        logger.debug(f"Processing user query: {user_query}")
        response = llm_client.infer(
            system_prompt=misleading_agent_system_prompt,
            user_prompt=misleading_agent_user_prompt.format(user_query=user_query),
            messages=state['messages']
        )

        input_token=response.usage_metadata['input_tokens']
        output_token=response.usage_metadata['output_tokens']
        total_tokens=response.usage_metadata['total_tokens']    
        insert_token_tracking(user_query, "misleading_agent", "misleading_agent_node", input_token, output_token, total_tokens)

        model_output = response.content
        logger.info(f"Misleading agent output: {model_output}")

        return {
            "model_output": model_output,
            "messages":[response]
        }
    except Exception as e:
        logger.error(f"Error in misleading agent: {str(e)}")
        raise e



