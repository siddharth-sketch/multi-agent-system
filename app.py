import streamlit as st
import requests
import time

# FastAPI endpoint URLs
API_QUERY_URL = "http://localhost:8000/user_query"
API_TOKEN_TRACKING_URL = "http://localhost:8000/token_tracking"
API_CONVERSATION_HISTORY_URL = "http://localhost:8000/conversation_history"

st.title("Multi-Agent System Interface")

# --- User Query Section ---
st.header("Ask a Question")

user_query = st.text_input("Enter your query:")

if st.button("Submit Query"):
    if user_query:
        start_time = time.time()
        with st.spinner("Processing..."):
            try:
                response = requests.get(API_QUERY_URL, params={"user_query": user_query})
                response.raise_for_status()
                result = response.json()
                end_time = time.time()
                execution_time = end_time - start_time
                st.success("Query Processed!")
                st.write(f"### Time taken: {execution_time:.2f} seconds")
                st.write("### Result:")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a query first.")

# --- Token Tracking Section ---
st.header("Token Tracking Records")

if st.button("Fetch Token Tracking"):
    with st.spinner("Fetching token tracking records..."):
        try:
            response = requests.get(API_TOKEN_TRACKING_URL)
            response.raise_for_status()
            result = response.json()
            if result["status"] == "success":
                # Convert data to DataFrame and display as table
                import pandas as pd
                df = pd.DataFrame(result["data"])
                st.table(df)
                st.success("Records retrieved successfully!")
            else:
                st.warning(f"Failed to retrieve records: {result.get('message')}")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Conversation History Section ---
st.header("Conversation History")

if st.button("View Conversation History"):
    with st.spinner("Fetching conversation history..."):
        try:
            response = requests.get(API_CONVERSATION_HISTORY_URL)
            response.raise_for_status()
            result = response.json()
            if result["status"] == "success":
                st.write("### Conversation History:")
                for message in result["history"]:
                    st.write(message)
                st.success("History retrieved successfully!")
            else:
                st.warning(f"Failed to retrieve history: {result.get('message')}")
        except Exception as e:
            st.error(f"Error: {e}")
