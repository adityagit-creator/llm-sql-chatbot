import streamlit as st, requests, os, pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.set_page_config(page_title="LLM SQL Chatbot", layout="wide")
st.title("🤖 LLM SQL Chatbot")

if "query_history" not in st.session_state:
    st.session_state.query_history = []

with st.sidebar:
    st.header("Query History")
    if st.session_state.query_history:
        df = pd.DataFrame(st.session_state.query_history)
        df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        st.dataframe(df[["timestamp", "query", "results"]], hide_index=True)
    if st.button("Clear History", use_container_width=True):
        st.session_state.query_history = []
        st.rerun()

query = st.text_area("Enter your query", height=150)
case = st.checkbox("Case sensitive")

if st.button("🚀 Execute Query"):
    if not query: st.warning("Please enter a query"); st.stop()
    with st.spinner("Processing..."):
        try:
            res = requests.post(
                f"{BASE_URL}/query",
                headers={"X-API-Key": API_KEY},
                json={"query": query, "case_sensitive": case},
                timeout=60
            )
            if res.status_code == 200:
                data = res.json()
                st.session_state.query_history.append({
                    "query": query,
                    "sql": data["sql_query"],
                    "results": len(data["results"]),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success(f"{data['message']} in {data['execution_time']}s")
                st.code(data["sql_query"], language="sql")
                if data["results"]:
                    st.dataframe(pd.DataFrame(data["results"]))
                else:
                    st.warning("No results found.")
            else:
                err = res.json().get("detail", "Unknown error")
                st.error(f"API Error: {err}")
        except Exception as e:
            st.error(f"Error: {e}")
