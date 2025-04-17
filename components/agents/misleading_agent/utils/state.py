from langgraph.graph import MessagesState

class State(MessagesState):
    user_query: str
    model_output: str
