# from pypdf import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import AzureOpenAIEmbeddings
# from qdrant_client import QdrantClient
# from qdrant_client.http.models import Distance, VectorParams
# from qdrant_client.http.models import PointStruct, Distance, VectorParams
# import numpy as np
# import uuid

# pdf_path = r"C:\Users\SiddharthMishra\Downloads\e&_Monitoring.pdf"

# temp=""
# reader = PdfReader(pdf_path)
# # page 2: Azure Application Insight
# pages={"Application_Insight_logs":[],"Database_Logs_Analysis":[],"How_to_trace_any_error":[],"How_to_capture_traces_through_SQL_Table":[]}
# for i,page in enumerate(reader.pages):
#     text = page.extract_text().strip() 
    
#     if(i in [4,5,6]):
#         temp+=text
#     if(i==7):
#         temp+=text
#         pages['How_to_trace_any_error'].append(text)
#     elif(i == 2):
#         pages['Application_Insight_logs'].append(text)
#     elif(i==8):
#         pages['How_to_capture_traces_through_SQL_Table'].append(text)
#     elif(i==3):
#         pages["Database_Logs_Analysis"].append(text)

# client_ = QdrantClient(
#     url="https://408d4eee-81fe-427f-a8cb-128923dc1053.us-east4-0.gcp.cloud.qdrant.io:6333", 
#     api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.oipZao46XuR3g0FD7uj70JwPTU-AOxv6aJWBStqy9DQ",
# )  

# client_.create_collection(  
#     collection_name="Etisalat_approach1", # collection is like a table in database
#     vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
# )

# embedder = AzureOpenAIEmbeddings(
#     azure_deployment="text-embedding-ada-002",  
#     azure_endpoint="https://ctcdpopenai.openai.azure.com", 
#     api_key="90cd41786f514166b0414b05a5e9eb5c", 
#     api_version="2024-06-01" 
# )

# embedding={}
# for topic in pages:
#     page_title=topic
#     data_for_title=pages[topic]
#     embedding[page_title]=embedder.embed_documents(data_for_title)

# documents_2=[]
# page_num=2
# id=1
# for i,title in enumerate(pages):
#     topic=title
#     text=pages[topic]
#     for i,data in enumerate(text):
#         documents_2.append({"id":id , "text":data, "vector" : embedding[topic][i], "title":topic,"page_num":page_num})
#         page_num+=1
#         id+=1
    

# client_.upsert(
#     collection_name="Etisalat_approach1",
#     points=[
#         PointStruct(
#             id=doc["id"],
#             vector=doc["vector"],  
#             payload={"page_num": doc["page_num"],"text": doc["text"],"title": doc["title"]},  # Metadata
#         )
#         for doc in documents_2
#     ],
# )

# print("done")


