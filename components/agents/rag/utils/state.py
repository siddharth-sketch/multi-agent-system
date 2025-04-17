from langgraph.graph import MessagesState

class state(MessagesState):
    model_output: str
    user_query :str