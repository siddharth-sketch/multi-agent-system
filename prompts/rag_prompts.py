system_prompt = '''
### TASK ###
- You will be given a user query and you have option to use tools if required for the extra context of user query.
- The tool has information about:
    -> The PDF provides a guide on how to trace logs, errors, and application activity using:
        1. Azure Application Insights:
            - Signing into the Azure Portal
            - Locating the Application Insights resource
            - Accessing logs, traces, requests, and exceptions
            - Reviewing trace logs and severity levels
        2. Unified UI:
            - Logging into the unified platform
            - Locating and drilling into transaction logs 
            - Analyzing log information
        3. FAQs:
            - How to trace any error?
            - How to capture traces using SQL tables?
- So whenever you have a user query that is related to the PDF context mentioned above, you can call the RAG tool to get extra context.
'''

user_prompt = '''
### USER QUERY ###
{user_query}
'''