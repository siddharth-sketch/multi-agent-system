from langgraph.graph import MessagesState

class State(MessagesState):
    user_query: str # user query
    agent_name : str # name of the agent
    agent_output : str # output of the agent
