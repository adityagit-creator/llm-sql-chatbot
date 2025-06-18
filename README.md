# llm-sql-chatbot
# LLM-Powered Chatbot with FastAPI and SQL Integration

A complete solution for the LLM-powered chatbot problem statement that converts natural language queries to SQL using Groq's LLM API and FastAPI backend.

## Problem Statement Implementation

This project implements a chatbot application that:
- Takes free-text queries from users
- Uses Groq-hosted LLM (LLAMA 4) to interpret queries
- Generates corresponding SQL queries
- Executes queries against a SQLite customer database
- Returns formatted results to the user

## Features

- ✅ FastAPI backend with RESTful API
- ✅ Natural language to SQL conversion using Groq's Llama3-70b model
- ✅ SQLite database with customer schema as specified
- ✅ Streamlit web interface (alternative to ReactJS)
- ✅ Comprehensive logging and error handling
- ✅ API security with token-based authentication
- ✅ Environment variable configuration

## Setup Instructions

### Prerequisites

- Python 3.8+
- Groq API key (free tier available at https://groq.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone <https://github.com/adityagit-creator/llm-sql-chatbot>
   cd llm-sql-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   API_KEY=your_secure_api_key_here
   ```

4. **Initialize Database** (Optional - auto-created on startup)
   ```bash
   sqlite3 customers.db < schema_seed.sql
   ```

### Running the Application

1. **Start the FastAPI Backend**
   Terminal 1 - FastAPI backend
   ```bash
   uvicorn main:app --reload

   ```
   The API will be available at `http://localhost:8000`

2. **Start the Streamlit Frontend**
   (in a new terminal)
   Terminal 2 - Streamlit frontend
    streamlit run app.py 
   ```bash
   streamlit run app.py
   ```
   The web interface will open at `http://localhost:8501`

## API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Query Endpoint
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"query": "show me all female customers from Mumbai", "case_sensitive": false}'
```
## Deliverables ✅

All required deliverables are included:

- ✅ **FastAPI backend code** (`main.py`)
- ✅ **SQLite schema and seed script** (`schema_seed.sql`)
- ✅ **Frontend UI** (`app.py` - Streamlit alternative to ReactJS)
- ✅ **ReadMe file** (this file) with setup and run instructions
- ✅ **Requirements file** (`requirements.txt`)
- ✅ **All code committed to public GitHub profile**

  
## Expected Functionality ✅

The application implements all required functionality:

1. **User Input**: Natural language queries via web UI
   - Example: "Show me all female customers from Mumbai"

2. **LLM Processing**: Backend sends query to Groq LLM endpoint
   - Uses Llama4 model via Groq API

3. **SQL Generation**: LLM interprets query and generates SQL
   - Converts natural language to valid SQLite queries

4. **Query Execution**: Backend executes SQL and retrieves results
   - Secure execution with validation and error handling

5. **Response Display**: Frontend displays formatted results
   - Results shown in tabular format with query history

## Bonus Features Implemented ✅

- **Comprehensive Logging**: All queries and SQL generation logged to `chatbot.log`
- **Advanced Error Handling**: Invalid queries, SQL errors, and API failures handled gracefully
- **Environment Variables**: All configuration via `.env` file for security
- **API Security**: Token-based authentication for all endpoints
- **Query History**: Session-based history tracking in UI
- **SQL Injection Protection**: Query validation and sanitization
- **Performance Optimization**: Database indexing on frequently queried columns

## Example Queries

Try these natural language queries:
- "Show me all female customers from Mumbai"
- "Find male customers from New York" 
- "List customers in Mumbai or London"
- "Show all customers"
- "Female customers from Mumbai and male from Paris"

## Database Schema (As Required)

The application implements the exact schema specified in the problem statement:

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Primary Key
    name TEXT NOT NULL,                             -- Text
    gender TEXT,                                    -- Text  
    location TEXT                                   -- Text
);
```

```**Sample Data**: Pre-seeded with 10+ customer entries as required (minimum 5).```

### Postman Testing Instructions

Since we provide a Streamlit frontend instead of ReactJS, here are Postman test instructions as mentioned in the requirements:

#### 1. Health Check
```
GET http://localhost:8000/health
```

#### 2. Query Endpoint
```
POST http://localhost:8000/query
Headers:
  Content-Type: application/json
  X-API-Key: your_api_key_here

Body (JSON):
{
    "query": "Show me all female customers from Mumbai",
    "case_sensitive": false
}
```

#### Sample Postman Collection
Create these requests in Postman:

1. **Health Check**
   - Method: GET
   - URL: `{{base_url}}/health`

2. **Female customers from Mumbai**
   - Method: POST
   - URL: `{{base_url}}/query`
   - Headers: `X-API-Key: {{api_key}}`
   - Body: `{"query": "Show me all female customers from Mumbai"}`

3. **Male customers from New York**
   - Method: POST
   - URL: `{{base_url}}/query`
   - Headers: `X-API-Key: {{api_key}}`
   - Body: `{"query": "Find male customers from New York"}`

Environment variables:
- `base_url`: `http://localhost:8000`
- `api_key`: Your API key from `.env` file

## Tech Stack (As Per Requirements)

- **Backend**: FastAPI ✅
- **Frontend**: Streamlit (alternative to ReactJS - provides better UX)
- **Database**: SQLite3 ✅
- **LLM Endpoint**: Groq (free tier) using Llama4 model ✅
- **Authentication**: Token-based API security ✅

## Troubleshooting

1. **Database connection errors**: Ensure SQLite3 is installed
2. **LLM API errors**: Check your Groq API key is valid
3. **Import errors**: Run `pip install -r requirements.txt`

## Development Notes & Architecture

- **Auto Database Creation**: SQLite database auto-created on first run
- **LLM Model**: Uses Llama4 for optimal natural language processing
- **Security**: SQL injection prevention through query validation
- **Performance**: Indexed database columns for faster queries
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Graceful handling of all error scenarios

## Project Structure

```
llm-sql-chatbot/
├── main.py              # FastAPI backend
├── app.py               # Streamlit frontend
├── requirements.txt     # Python dependencies
├── schema_seed.sql      # Database schema and seed data
├── README.md            # Project documentation
├── customers.db         # SQLite database (auto-created)
├── .env                 # Environment variables (create this)      
├── chatbot.log          # Main application logs
├── chatbot_errors.log   # Error tracking
    
```

## Compliance with Requirements

This implementation fully meets the problem statement requirements:

- ✅ **Tech Stack**: FastAPI backend, database integration, Groq LLM
- ✅ **Database Schema**: Exact schema with customer_id, name, gender, location
- ✅ **Functionality**: Natural language → LLM → SQL → Results → Display
- ✅ **Bonus Features**: Logging, error handling, environment variables, security
- ✅ **Deliverables**: All code, documentation, and setup instructions provided
