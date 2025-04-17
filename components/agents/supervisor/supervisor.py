from components.agents.supervisor.utils.sup_state import State
from langgraph.graph import StateGraph, END, START
from components.agents.supervisor.utils.conditional_edges import agent_selection
from components.agents.supervisor.utils.nodes import supervisor_agent, text2sql_agent, rag_agent, web_search_agent, misleading_agent
from objects import memory
graph_builder = StateGraph(State)


graph_builder.add_node("supervisor",supervisor_agent)
graph_builder.add_node("text_to_sql",text2sql_agent)
graph_builder.add_node("rag",rag_agent)
graph_builder.add_node("web_search",web_search_agent)
graph_builder.add_node("misleading",misleading_agent)
graph_builder.add_edge(START, "supervisor" )
graph_builder.add_conditional_edges(
    "supervisor",
    agent_selection,
    {
        "TEXT_TO_SQL": "text_to_sql",
        "RAG": "rag",
        "WEB_SEARCH": "web_search",
        "MISLEADING": "misleading"
    }
)
graph_builder.add_edge("text_to_sql", END)
graph_builder.add_edge("rag", END)
graph_builder.add_edge("web_search", END)
graph_builder.add_edge("misleading", END)

app_supervisor=graph_builder.compile(checkpointer=memory)









