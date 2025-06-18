# main.py - FastAPI Backend
from fastapi import FastAPI, HTTPException, Depends, Security, Request
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sqlite3
import os
import logging
import time
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
from contextlib import contextmanager
import re

# Load environment variables
load_dotenv()

# Logging configuration with separate error log
logger = logging.getLogger("chatbot")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# General log file (all logs)
info_handler = logging.FileHandler("chatbot.log")
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

# Error-specific log file
error_handler = logging.FileHandler("chatbot_error.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# Console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Attach handlers
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)


app = FastAPI(
    title="LLM-Powered Chatbot API",
    description="API for processing natural language queries with LLM and SQL integration",
    version="1.3.0"  # Updated version
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY not configured")
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# Database setup
@contextmanager
def get_db_connection():
    try:
        conn = sqlite3.connect('customers.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Models
class UserQuery(BaseModel):
    query: str
    case_sensitive: bool = False

class QueryResponse(BaseModel):
    sql_query: str
    results: List[Dict[str, Any]]
    message: str
    execution_time: float

# LLM Client
def get_groq_client():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not configured")
    return Groq(api_key=groq_api_key)

# SQL Validation - Updated to allow complex SELECTs
def validate_sql_query(sql_query: str):
    # Remove trailing semicolon if present
    sql_query = sql_query.rstrip(';').strip()
    
    # Check for forbidden operations
    forbidden_keywords = ["insert", "update", "delete", "drop", "alter", "create", "truncate"]
    pattern = r'\b(' + '|'.join(forbidden_keywords) + r')\b'
    if re.search(pattern, sql_query, re.IGNORECASE):
        raise ValueError("Query contains forbidden SQL operation")
    
    # Check for multiple queries
    if ';' in sql_query:
        raise ValueError("Multiple queries not allowed")
    
    # Ensure it's a SELECT query
    if not re.match(r'^\s*select\s+', sql_query, re.IGNORECASE):
        if not re.match(r'^\s*with\s+', sql_query, re.IGNORECASE):
            raise ValueError("Only SELECT queries are allowed")

# Extract SQL from LLM response - Improved parsing
def extract_sql_from_response(response: str) -> str:
    # Check for code blocks
    if '```sql' in response:
        parts = response.split('```sql')
        if len(parts) > 1:
            sql = parts[1].split('```')[0].strip()
            return sql
    
    # Check for plain SQL
    if re.search(r'\b(select|from|where|join|group by|order by)\b', response, re.IGNORECASE):
        return response.strip()
    
    # Fallback to entire response
    return response.strip()

# SQL Generation - Updated for better natural language handling
def generate_sql_from_natural_language(query: str, case_sensitive: bool = False) -> str:
    try:
        client = get_groq_client()
        
        # Pre-process query to handle common variations
        processed_query = query.lower()
        processed_query = re.sub(r'\bcustomer(s)?\b', '', processed_query)  # Remove "customer/customers"
        processed_query = re.sub(r'\bfrom location\b', 'from', processed_query)  # Fix "from location"
        processed_query = processed_query.strip()
        
        prompt = f"""
        Convert this natural language query to SQL for SQLite:
        Original Query: "{query}"
        Processed Query: "{processed_query}"
        
        Database schema:
        Table: customers
        Columns: 
          - customer_id (INTEGER PRIMARY KEY)
          - name (TEXT)
          - gender (TEXT)
          - location (TEXT)
        
        Important Rules:
        1. Only return the SQL query
        2. Use {'case-sensitive' if case_sensitive else 'case-insensitive'} matching
        3. Only SELECT queries allowed (can include WHERE, AND, OR, etc.)
        4. Table name is always 'customers'
        5. Never include semicolons
        6. Handle natural language variations:
           - "customer" and "customers" both refer to the table
           - "from location X" means "WHERE location = 'X'"
           - "male" or "female" should map to gender column
        7. Always use exact matches (= operator) unless specified otherwise
        
        Examples:
        - "show me all female customer from location mumbai" 
          → SELECT * FROM customers WHERE gender = 'Female' AND location = 'Mumbai'
        - "show me all male customer from newyork" 
          → SELECT * FROM customers WHERE gender = 'Male' AND location = 'New York'
        - "find customers in mumbai or london" 
          → SELECT * FROM customers WHERE location IN ('Mumbai', 'London')
        - "list female customers from mumbai and male from paris"
          → SELECT * FROM customers WHERE (gender = 'Female' AND location = 'Mumbai') OR (gender = 'Male' AND location = 'Paris')
        
        Now generate SQL for: "{query}"
        """
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
            temperature=0.1,
            max_tokens=512
        )
        
        llm_response = chat_completion.choices[0].message.content.strip()
        logger.info(f"LLM raw response: {llm_response}")
        
        sql_query = extract_sql_from_response(llm_response)
        logger.info(f"Extracted SQL: {sql_query}")
        
        validate_sql_query(sql_query)
        return sql_query
        
    except Exception as e:
        logger.error(f"SQL generation failed: {str(e)}")
        raise HTTPException(
            status_code=400, 
            detail=f"SQL generation error: {str(e)}"
        )

# API Endpoints
@app.post("/query")
async def process_query(
    user_query: UserQuery,
    api_key: str = Depends(get_api_key)
) -> QueryResponse:
    start_time = time.time()
    logger.info(f"Received query: {user_query.query}")
    
    try:
        # Generate SQL
        sql_query = generate_sql_from_natural_language(
            user_query.query, 
            user_query.case_sensitive
        )
        logger.info(f"Generated SQL: {sql_query}")
        
        # Execute SQL
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql_query)
                results = [dict(row) for row in cursor.fetchall()]
            except sqlite3.Error as e:
                logger.error(f"SQL execution error: {str(e)}")
                raise HTTPException(
                    status_code=400, 
                    detail=f"SQL execution error: {str(e)}"
                )
        
        exec_time = time.time() - start_time
        logger.info(f"Query successful, execution time: {exec_time:.2f}s")
        
        return QueryResponse(
            sql_query=sql_query,
            results=results,
            message=f"Found {len(results)} results",
            execution_time=exec_time
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception("Query processing failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM customers")
            count = cursor.fetchone()[0]
        
        return {
            "status": "healthy",
            "database_records": count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

# Database initialization
def init_db():
    if not os.path.exists('customers.db'):
        with sqlite3.connect('customers.db') as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                gender TEXT,
                location TEXT
            )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX idx_customers_location ON customers(location)")
            cursor.execute("CREATE INDEX idx_customers_gender ON customers(gender)")
            
            # Sample data
            customers = [
                ("John Doe", "Male", "New York"),
                ("Jane Smith", "Female", "Mumbai"),
                ("Alice Johnson", "Female", "London"),
                ("Bob Brown", "Male", "Mumbai"),
                ("Charlie Davis", "Male", "Paris"),
                ("Diana Evans", "Female", "Mumbai"),
                ("Eve Wilson", "Female", "Tokyo")
            ]
            
            cursor.executemany(
                "INSERT INTO customers (name, gender, location) VALUES (?, ?, ?)",
                customers
            )
            
            conn.commit()

@app.on_event("startup")
def startup():
    init_db()
    logger.info("Application started")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)