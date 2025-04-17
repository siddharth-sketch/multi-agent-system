# node1
from prompts.text2sql_prompts import (
    intent_system_prompt,
    user_prompt,
    data_assistance_system_prompt,
    user_prompt2,
    misleading_query_system_prompt,
    user_prompt3,
    text_to_sql_system_prompt,
    user_prompt4,
    verify_sql_system_prompt,
    user_prompt5,
    recreate_sql_system_prompt,
    user_prompt6
    )
from data.metadata.structured import schema,knowledge_graph
from components.agents.text2sql.utils.state import State
from objects import llm_client,sqlite_client
import json
import sqlite3
from langchain_core.messages import AIMessage
from logger_ import logger
from database.sqlite import insert_token_tracking

##TODO: Need to capture tokens count from the output of each LLM

def intent_classifier_node(state: State):
    '''
    Intent Classifier Function
    
    This function takes a State object as input and classifies the user's query intent.
    It uses an LLM to determine if the query is database-related or conversational.
    
    Args:
        state (State): A TypedDict containing the current conversation state
                      Must include 'user_query' key with the user's input text
                      
    Returns:
        state (State): Updated state with 'intent' key containing the classified intent
                      Intent includes rephrased question, reasoning and results
                      
    The function:
    1. Extracts the user query from state
    2. Sends query to LLM with system and user prompts
    3. Parses JSON response and adds intent classification to state
    '''
    try:
        logger.info("Starting intent classification")

        user_query = state["user_query"]
        logger.debug(f"Processing user query: {user_query}")

        response = llm_client.infer(system_prompt=intent_system_prompt,
                                  user_prompt=user_prompt.format(user_query=user_query,schema=schema))
        
        response_json = json.loads(response.content)

        input_token=response.usage_metadata['input_tokens']
        output_token=response.usage_metadata['output_tokens']
        total_tokens=response.usage_metadata['total_tokens']
        insert_token_tracking(user_query, "Text2SQL", "intent_classifier_node", input_token, output_token, total_tokens)

        logger.info("Successfully classified intent")
        
        return {"intent":response_json['results'], "iteration_count":0,"messages":[response]}
    except Exception as e:
        logger.error(f"Error in intent classification: {str(e)}")
        raise e

# node2
def general_intent_node(state: State):
    '''
    General Intent Handler Function
    
    This function processes queries with general/conversational intent.
    It provides informative responses about database schema and structure.
    
    Args:
        state (State): A TypedDict containing the conversation state
                      Must include 'intent' and 'user_query' keys
                      
    Returns:
        state (State): Updated state with 'model_output' containing the response
                      
    The function:
    1. Gets intent and user query from state
    2. Sends to LLM with system and user prompts for general assistance
    3. Adds LLM response to state as model_output
    '''
    try:
        logger.info("Starting general intent processing")
        intent = state["intent"]
        user_query = state["user_query"]
        logger.debug(f"Processing query: {user_query} with intent: {intent}")

        response = llm_client.infer(system_prompt=data_assistance_system_prompt,
                                  user_prompt=user_prompt2.format(user_query=user_query,schema=schema,intent=intent))
        
        input_token=response.usage_metadata['input_tokens']
        output_token=response.usage_metadata['output_tokens']
        total_tokens=response.usage_metadata['total_tokens']
        insert_token_tracking(user_query, "Text2SQL", "general_intent_node", input_token, output_token, total_tokens)

        logger.info("Successfully processed general intent")
        return {"model_output": response.content,"messages":[response]}
    except Exception as e:
        logger.error(f"Error in general intent processing: {str(e)}")
        raise e

# node 3 
def mislead_intent_node(state: State):
    '''
    Misleading Intent Handler Function
    
    This function processes queries identified as potentially misleading or problematic.
    It provides appropriate responses to redirect or clarify such queries.
    
    Args:
        state (State): A TypedDict containing the conversation state
                      Must include 'intent' and 'user_query' keys
                      
    Returns:
        state (State): Updated state with 'model_output' containing the response
                      
    The function:
    1. Gets intent and user query from state
    2. Sends to LLM with system and user prompts for handling misleading queries
    3. Adds LLM response to state as model_output
    '''
    try:
        logger.info("Starting misleading intent processing")
        intent = state["intent"]
        user_query = state["user_query"]
        logger.debug(f"Processing potentially misleading query: {user_query}")

        response = llm_client.infer(system_prompt=misleading_query_system_prompt,
                                  user_prompt=user_prompt3.format(user_query=user_query,intent=intent),messages=state['messages'])
        
        input_token=response.usage_metadata['input_tokens']
        output_token=response.usage_metadata['output_tokens']
        total_tokens=response.usage_metadata['total_tokens']
        insert_token_tracking(user_query, "Text2SQL", "mislead_intent_node", input_token, output_token, total_tokens)

        logger.info("Successfully processed misleading intent")
        return {"model_output": response.content,"messages":[response]}
    except Exception as e:
        logger.error(f"Error in misleading intent processing: {str(e)}")
        raise e

#node4
def text_to_sql_node(state: State):
    '''
    Text to SQL Conversion Function
    
    This function converts user's natural language query into an SQL query.
    It uses an LLM to generate the SQL query based on the user's query and database schema.
    
    Args:
        state (State): A TypedDict containing the conversation state
                    Must include 'user_query' key with the user's input text
                    
    Returns:
        state (State): Updated state with 'sql_query' key containing the generated SQL query
    '''
    try:
        logger.info("Starting text to SQL conversion")
        user_query = state["user_query"]
        intent = state["intent"]
        logger.debug(f"Converting query: {user_query} to SQL")

        response = llm_client.infer(system_prompt=text_to_sql_system_prompt,
                                  user_prompt=user_prompt4.format(user_query=user_query,intent=intent,schema=schema,knowledge_graph=knowledge_graph))
        
        input_token=response.usage_metadata['input_tokens']
        output_token=response.usage_metadata['output_tokens']
        total_tokens=response.usage_metadata['total_tokens']
        insert_token_tracking(user_query, "Text2SQL", "text_to_sql_node", input_token, output_token, total_tokens)

        try:
            response_json = json.loads(response.content)
            logger.info("Successfully converted text to SQL")
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            response_json = {
                "verified": False,
                "reasoning": f"Invalid JSON format returned by LLM: {e}"
            }
            
        if response_json["sql_query"]:
            return {"sql_query":response_json["results"],"messages":[response]}
        else:
            return {"model_output": response_json["reasoning"],"messages":[response]}
    except Exception as e:
        logger.error(f"Error in text to SQL conversion: {str(e)}")
        raise e
    
#node5
def verify_sql_node(state: State):
    '''
    SQL Query Verification Function
    
    This function verifies the generated SQL query against the user's query and intent.
    It uses an LLM to check if the query is correct and meets the user's intent.
    
    Args:
        state (State): A TypedDict containing the conversation state
                      Must include 'sql_query' and 'user_query' keys
                      
    Returns:
        state (State): Updated state with 'sql_query_verified' key containing the verification result

    The function:
    1. Gets SQL query and user query from state
    2. Sends to LLM with system and user prompts for verification
    3. Parses JSON response and adds verification result to state
    '''
    try:
        logger.info("Starting SQL verification")
        sql_query = state["sql_query"]
        user_query = state["user_query"]
        intent = state["intent"]
        logger.debug(f"Verifying SQL query: {sql_query}")
        
        response = llm_client.infer(system_prompt=verify_sql_system_prompt,
                                  user_prompt=user_prompt5.format(sql_query=sql_query,user_query=user_query,intent=intent,schema=schema,knowledge_graph=knowledge_graph))
        
        input_token=response.usage_metadata['input_tokens']
        output_token=response.usage_metadata['output_tokens']
        total_tokens=response.usage_metadata['total_tokens']
        insert_token_tracking(user_query, "Text2SQL", "verify_sql_node", input_token, output_token, total_tokens)

        try:
            response_json = json.loads(response.content)
            logger.info("Successfully verified SQL query")
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            response_json = {
                "verified": False,
                "reasoning": f"Invalid JSON format returned by LLM: {e}"
            }
            
        return {
                "sql_query_verified":response_json["verified"],
                "verified_reasoning": response_json["reasoning"],
                "messages":[response]
            }
    except Exception as e:
        logger.error(f"Error in SQL verification: {str(e)}")
        raise e
    
#node6
def execute_sql_node(state: State):
    '''
    SQL Query Execution Function
    
    This function executes the generated SQL query and returns the results.
    It uses SQLite to execute the query and return the results in JSON format.
    
    Args:
        state (State): A TypedDict containing the conversation state
                      Must include 'sql_query' key with the generated SQL query
                      
    Returns:
        state (State): Updated state with 'model_output' containing the query results

    The function:
    1. Connects to SQLite database
    2. Executes the SQL query
    3. Converts results to JSON string
    4. Returns JSON string and updates state with execution results
    '''
    try:
        logger.info(f"Starting SQL execution:{state['sql_query']}")
        conn = sqlite3.connect('etisalat_sales.db')
        logger.debug("Database connection established")
        
        sql_query = state["sql_query"]
        # print()
        logger.debug(f"Executing SQL query: {sql_query}")
        
        data = []
        try:
            rows = conn.execute(sql_query)
            for row in rows:
                data.append(row)
        
            json_string = json.dumps(data)
            logger.info("Successfully executed SQL query")
            conn.close()
            return {'model_output':json_string,
                    'messages':[AIMessage(content=json_string,name='sql_query_results')],
                    'execution_error':False,
                    'error_message':''}
            
        except Exception as e:
            logger.error(f"SQL execution error: {str(e)}")
            conn.close()
            return {'model_output':'',
                    'messages':[AIMessage(content=str(e),name='sql_query_results')],
                    'execution_error':True,
                    'error_message':str(e)}
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise e

# node7
def recreate_sql(state: State):
    try:
        logger.info("Starting SQL query recreation")
        sql_query = state["sql_query"]
        user_query = state["user_query"]
        verified_reasoning = state["verified_reasoning"]
        logger.debug(f"Recreating SQL query: {sql_query}")

        response = llm_client.infer(system_prompt=recreate_sql_system_prompt,
                                  user_prompt=user_prompt6.format(sql_query=sql_query,user_query=user_query,verified_reasoning=verified_reasoning,schema=schema,knowledge_graph=knowledge_graph))
        
        input_token=response.usage_metadata['input_tokens']
        output_token=response.usage_metadata['output_tokens']
        total_tokens=response.usage_metadata['total_tokens']
        insert_token_tracking(user_query, "Text2SQL", "recreate_sql_node", input_token, output_token, total_tokens)

        try:
            response_json = json.loads(response.content)
            logger.info("Successfully recreated SQL query")
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.debug(f"Raw response content: {repr(response.content)}")
            response_json = {
                "verified": False,
                "reasoning": f"Invalid JSON format returned by LLM: {e}"
            }

        return {"sql_query":response_json['recreated_sql_query'],"messages":[response]}
    except Exception as e:
        logger.error(f"Error in SQL recreation: {str(e)}")
        raise e
