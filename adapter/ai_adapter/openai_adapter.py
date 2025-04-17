from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os
from core.model import llm
from logger_ import logger
load_dotenv()

class AzureopenAi_(llm):
    def __init__(self,model_name):
        try:
            self.api_key=os.getenv("AZURE_OPENAI_API_KEY")
            self.azure_endpoint=os.getenv("AZURE_ENDPOINT")
            self.openai_api_version=os.getenv("OPENAI_API_VERSION")
            self.model_name=model_name
            
            logger.info(f"Initializing AzureOpenAI client with model: {model_name}")
            
            self.client=AzureChatOpenAI(
                                api_key=self.api_key,
                                api_version=self.openai_api_version,
                                azure_endpoint=self.azure_endpoint,
                                name=self.model_name
                            )
            logger.info("AzureOpenAI client initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing AzureOpenAI client: {str(e)}")
            raise e
    
    def infer(self,system_prompt,user_prompt,messages:list = []):
        try:
            logger.info("Starting inference with AzureOpenAI")
            message=messages+[
                    ("system",system_prompt),
                    ("user",user_prompt)
                ]
            response=self.client.invoke(message)
            logger.info("Inference completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error during inference: {str(e)}")
            logger.debug(f"System prompt: {system_prompt}")
            logger.debug(f"User prompt: {user_prompt}")
            raise e