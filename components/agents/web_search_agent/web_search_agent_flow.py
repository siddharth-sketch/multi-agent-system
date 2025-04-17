from langgraph.graph import StateGraph, START, END 
from components.agents.web_search_agent.utils.state import State
from langgraph.prebuilt import tools_condition
from langchain_core.tools import  tool
from langchain_openai import AzureChatOpenAI
from components.agents.web_search_agent.utils.nodes import web_agent
from components.tools.web_search_tool  import tool_node
from objects import memory

llm = AzureChatOpenAI()
graph_builder = StateGraph(State)



graph_builder.add_node("node3",web_agent)

graph_builder.add_node("tool_node",tool_node)

graph_builder.add_edge(START,"node3")
graph_builder.add_conditional_edges(
    "node3",
    tools_condition,
    {"tools": "tool_node", END: END}
    )
graph_builder.add_edge("tool_node","node3")
app_web_agent = graph_builder.compile(checkpointer=memory)