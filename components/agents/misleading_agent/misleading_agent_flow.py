from components.agents.misleading_agent.utils.nodes import misleading_agent
from components.agents.misleading_agent.utils.state import State
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, END, START
from objects import memory


graph_builder = StateGraph(State)

graph_builder.add_node("misleading_agent",misleading_agent)

graph_builder.add_edge(START, "misleading_agent")
graph_builder.add_edge("misleading_agent", END)

app_misleading_agent = graph_builder.compile(checkpointer=memory)





