from components.agents.supervisor.utils.sup_state import State


def agent_selection(state: State):
    if state["agent_name"] == "text2sql":
        return "TEXT_TO_SQL"
    elif state["agent_name"] == "rag":
        return "RAG"
    elif state["agent_name"] == "web_search":
        return "WEB_SEARCH"
    elif state["agent_name"] == "misleading":
        return "MISLEADING"

