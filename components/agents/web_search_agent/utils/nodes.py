from components.agents.web_search_agent.utils.state import State
from langchain_core.messages.tool import ToolMessage
import json
from objects import llm_client
from components.tools.web_search_tool import web_tools
from prompts.web_search import user_prompt,system_prompt,system_prompt2
from logger_ import logger
from database.sqlite import insert_token_tracking

llm_with_tools = llm_client.client.bind_tools(tools=web_tools)

def web_agent(state: State):
    try:
        logger.info("Starting web agent processing")
        user_query = state['user_query']
        logger.debug(f"Processing user query: {user_query}")

        if(state['messages'].__len__()>0 and isinstance(state["messages"][-1],ToolMessage)):
            logger.info("Processing web agent response after tool call")
            try:
                data_str = state["messages"][-1].content
                data = json.loads(data_str)
                logger.debug(f"Received tool message content: {data_str}")

                url = []
                title = []
                content = []
                for i in data['results']:
                    url.append(i['url'])
                    title.append(i['title'])
                    content.append(i['content'])
                
                logger.debug("Extracted search results data")

                while len(url) < 3:
                    url.append("")
                while len(title) < 3:
                    title.append("")
                while len(content) < 3:
                    content.append("")

                response = llm_client.infer(
                    user_prompt=user_prompt.format(
                        url1=url[0], url2=url[1], url3=url[2],
                        title1=title[0], title2=title[1], title3=title[2],
                        content1=content[0], content2=content[1], content3=content[2]
                    ),
                    system_prompt=system_prompt2
                )
                logger.info("Successfully generated LLM response after tool call")

                input_token=response.usage_metadata['input_tokens']
                output_token=response.usage_metadata['output_tokens']
                total_tokens=response.usage_metadata['total_tokens']
                insert_token_tracking(user_query, "web_search_agent", "web_search_agent_node", input_token, output_token, total_tokens)

                return {"messages":[response],"model_output":response.content}

            except Exception as e:
                logger.error(f"Error processing tool response: {str(e)}")
                raise e

        logger.info("Generating initial LLM response")
        message=[("system",system_prompt),("user",user_query)]
        try:
            response = llm_with_tools.invoke(message)
            logger.info("Successfully generated initial LLM response")
            logger.debug(f"LLM Response: {response}")

            input_token=response.usage_metadata['input_tokens']
            output_token=response.usage_metadata['output_tokens']
            total_tokens=response.usage_metadata['total_tokens']
            insert_token_tracking(user_query, "web_search_agent", "web_search_agent_node", input_token, output_token, total_tokens)

            return {"messages":[response], "model_output":response.content}
        except Exception as e:
            logger.error(f"Error generating initial LLM response: {str(e)}")
            raise e

    except Exception as e:
        logger.error(f"Error in web agent: {str(e)}")
        raise e