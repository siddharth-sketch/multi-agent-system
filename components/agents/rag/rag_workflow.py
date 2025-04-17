from langgraph.graph import StateGraph, START, END 
from langgraph.prebuilt import ToolNode, tools_condition
from objects import memory
from components.tools.rag_tool import tool_node
from components.agents.rag.utils.state import state as State
from components.agents.rag.utils.nodes import rag_agent
from objects import llm_client
from components.tools.rag_tool import rag_tools
from logger_ import logger



graph_builder = StateGraph(State)

graph_builder.add_node("rag_agent_", rag_agent)
graph_builder.add_node("tools_node", tool_node) # rag_ : name of node, rag : name of tool => rag_ contain rag => node contain tool

graph_builder.add_edge(START, "rag_agent_")
graph_builder.add_conditional_edges(
    "rag_agent_",
    tools_condition,
    {"tools": "tools_node", END: END}
)

graph_builder.add_edge( "tools_node","rag_agent_" )

app_rag_agent = graph_builder.compile(checkpointer=memory)

llm_with_tools = llm_client.client.bind_tools(tools=rag_tools)
