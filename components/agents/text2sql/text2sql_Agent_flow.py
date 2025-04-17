from components.agents.text2sql.utils.state import State
from components.agents.text2sql.utils.nodes import (
    verify_sql_node,
    text_to_sql_node,
    intent_classifier_node,
    general_intent_node,
    mislead_intent_node,
    execute_sql_node,
    recreate_sql
)
from components.agents.text2sql.utils.conditional_edge import intent_condition, execution_check
from langgraph.graph import StateGraph, END, START
from objects import memory
    
graph_builder = StateGraph(State)


graph_builder.add_node("verify_sql",verify_sql_node)
graph_builder.add_node("text_to_sql",text_to_sql_node)
graph_builder.add_node("intent_classifier", intent_classifier_node)

graph_builder.add_node("general_intent",general_intent_node)
graph_builder.add_node("mislead_intent",mislead_intent_node)
graph_builder.add_node("execute_sql",execute_sql_node)
graph_builder.add_node("recreate_sql",recreate_sql)


graph_builder.add_edge(START, "intent_classifier" )
graph_builder.add_conditional_edges(
    "intent_classifier",
    intent_condition,
    {
        "GENERAL": "general_intent",
        "TEXT_TO_SQL": "text_to_sql",
        "MISLEADING": "mislead_intent",
    }
)

graph_builder.add_edge("general_intent", END)
graph_builder.add_edge("text_to_sql", "verify_sql")
graph_builder.add_conditional_edges(
    "verify_sql",
    execution_check,
    {
        "execute": "execute_sql",
        "recreate_sql" : "recreate_sql"
    }
)

# graph_builder.add_edge("verify_sql", END)
graph_builder.add_edge("mislead_intent", END)
graph_builder.add_edge("execute_sql", END)
graph_builder.add_edge("recreate_sql", "execute_sql")
app_text_2_sql=graph_builder.compile(checkpointer=memory)







