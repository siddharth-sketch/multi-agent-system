from langgraph.graph import MessagesState

class State(MessagesState):
    intent: str # describe the intent of the user query
    user_query : str # user query
    sql_query : str # sql query
    sql_query_verified : bool # if the sql query is correct or not
    verified_reasoning : str # reasoning if the sql query is not correct
    execution_error : bool # if the query is not able to execute
    error_message : str # error message
    iteration_count : int # number of iteration
    model_output : str # output of the model
    table_data : bool # tells if the model output have table data or not
    


