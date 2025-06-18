# app.py - Streamlit Frontend
import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import time

# Load environment variables
load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY")

def main():
    st.set_page_config(
        page_title="LLM SQL Chatbot",
        layout="wide",
        page_icon="🤖"
    )
    
    # Initialize session state
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    st.title("LLM-Powered SQL Chatbot")
    st.caption("Try queries like: 'show me all female customer from location mumbai' or 'male customer from newyork'")
    
    # Sidebar for history
    with st.sidebar:
        st.header("Query History")
        if st.session_state.query_history:
            history_df = pd.DataFrame(st.session_state.query_history)
            # Format timestamp for display
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            st.dataframe(history_df[['timestamp', 'query', 'results']], hide_index=True)
        else:
            st.info("No query history yet")
        
        # Clear history button
        if st.button("Clear History", use_container_width=True):
            st.session_state.query_history = []
            st.rerun()
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_area(
            "Enter your query:", 
            placeholder="e.g., Show me all female customer from location Mumbai",
            height=150,
            key="query_input"
        )
    
    with col2:
        case_sensitive = st.checkbox("Case sensitive matching")
        st.caption("Applies to text comparisons")
        st.write("")
        execute_btn = st.button("🚀 Execute Query", use_container_width=True)
    
    if execute_btn:
        if not query:
            st.error("Please enter a query")
            return
            
        with st.spinner("Processing your query..."):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{FASTAPI_URL}/query",
                    json={"query": query, "case_sensitive": case_sensitive},
                    headers={"X-API-Key": API_KEY},
                    timeout=60  # Increased timeout for complex queries
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Add to history
                    st.session_state.query_history.append({
                        'query': query,
                        'sql': data['sql_query'],
                        'results': len(data['results']),
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    st.success(f"Query executed in {data['execution_time']:.2f} seconds")
                    
                    # Display results
                    with st.expander("View SQL Query", expanded=True):
                        st.code(data['sql_query'], language="sql")
                    
                    if data['results']:
                        st.subheader(f"Results ({len(data['results'])} records)")
                        df = pd.DataFrame(data['results'])
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("No results found")
                        
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"API Error: {error_detail}")
                    
                    # Add to history with error
                    st.session_state.query_history.append({
                        'query': query,
                        'sql': f"ERROR: {error_detail}",
                        'results': 0,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()