from logger_ import logger
logger.info("------------------------------------------------------Starting the application------------------------------------------------------")
from fastapi import FastAPI
from components.agents.supervisor.supervisor import app_supervisor
from database.sqlite import show_token_tracking
app=FastAPI()

@app.get("/user_query")
def read_root(user_query:str):
    config = {"configurable": {"thread_id": "1"}}
    output=app_supervisor.invoke({"user_query":user_query},config)
    return output['agent_output']

@app.get("/token_tracking")
def get_token_tracking():
    try:
        logger.info("Retrieving token tracking records")
        records = show_token_tracking()
        logger.info("Successfully retrieved token tracking records")
        return {"status": "success", "data": records}
    except Exception as e:
        logger.error(f"Error retrieving token tracking: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/conversation_history")
def get_conversation_history():
    try:
        logger.info("Retrieving conversation history")
        config = {"configurable": {"thread_id": "1"}}
        output = app_supervisor.invoke({"user_query": "get_history"}, config)
        logger.info("Successfully retrieved conversation history")
        return {"status": "success", "history": output['messages']}
    except Exception as e:
        logger.error(f"Error retrieving conversation history: {str(e)}")
        return {"status": "error", "message": str(e)}
