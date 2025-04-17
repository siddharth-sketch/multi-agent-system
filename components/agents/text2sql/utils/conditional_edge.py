from components.agents.text2sql.utils.state import State
from logger_ import logger

def intent_condition(state: State):
    print(f"current intent is {state['intent']}")
    logger.info(f"current intent is {state['intent']}")
    if state["intent"] == "TEXT_TO_SQL":
        return "TEXT_TO_SQL"
    elif state["intent"] == "MISLEADING_QUERY":
        return "MISLEADING"
    else:
        return "GENERAL"

def execution_check(state: State):
    logger.info(f"execution checking : {state['sql_query_verified']},{state['verified_reasoning']}")
    if(state['sql_query_verified']):
        return "execute"
    else:
        return "recreate_sql"