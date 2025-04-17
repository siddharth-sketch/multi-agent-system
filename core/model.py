from abc import ABCMeta, abstractmethod 


class llm(metaclass=ABCMeta):
    def __init__(self,model_name):
        self.model_name=model_name
        
        
    @abstractmethod
    def infer(self, *arg, **kwargs):
        ...
 
        
class database(metaclass=ABCMeta):
    def __init__(self,*arg, **kwargs):
        ...
        
    def get_data(self,sql_query):
        ...
        
    def get_conn(self):
        ...
    