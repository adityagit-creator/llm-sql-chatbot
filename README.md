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

## Screenshots of project

### 1. Main Application Interface
![Main Interface](https://github.com/adityagit-creator/llm-sql-chatbot/blob/main/Screenshots/WhatsApp%20Image%202025-06-18%20at%2012.49.13_bd24809b.jpg)
*Streamlit frontend showing the query input area and history sidebar*

### 2. Query Processing and result display
![Query example](https://github.com/adityagit-creator/llm-sql-chatbot/blob/main/Screenshots/WhatsApp%20Image%202025-06-18%20at%2012.57.16_6905600e.jpg)

![Query example](https://github.com/adityagit-creator/llm-sql-chatbot/blob/main/Screenshots/WhatsApp%20Image%202025-06-18%20at%2012.57.59_bac37454.jpg)

![Query example](https://github.com/adityagit-creator/llm-sql-chatbot/blob/main/Screenshots/WhatsApp%20Image%202025-06-18%20at%2012.59.31_d13147fa.jpg)

![Query example](https://github.com/adityagit-creator/llm-sql-chatbot/blob/main/Screenshots/WhatsApp%20Image%202025-06-18%20at%2013.00.33_1e3d8a8b.jpg)

### 3. Query History
![Query History](https://github.com/adityagit-creator/llm-sql-chatbot/blob/main/Screenshots/Screenshot%202025-06-18%20145253.png)


## Features

- ✅ FastAPI backend with RESTful API
- ✅ Natural language to SQL conversion using Groq's Llama4 model
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
- ✅ **Error Handling**: Graceful handling of all error scenarios
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

- **Comprehensive Logging**: All queries and SQL generation logged to `chatbot.log` and `chatbot_error.log` .
- **Environment Variables**: All configuration via `.env` file for security
- **API Security**: Token-based authentication for all endpoints
- **Query History**: Session-based history tracking in UI

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

# Postman Test Instructions

This guide explains how to test the FastAPI-based LLM SQL Chatbot API using Postman, including environment variable setup and API authentication.

---

## 📦 1. Install Postman

Download and install Postman from [https://www.postman.com/downloads/](https://www.postman.com/downloads/).

---

## 📁 2. Create a New Collection

1. Open Postman.
2. Go to the **Collections** tab.
3. Click **New Collection**.
4. Name it `LLM SQL Chatbot API`.
5. Click **Create**.

---

## 🔐 3. Add Environment Variables

1. Click the **gear icon** (⚙️) in the top-right > choose **"Manage Environments"**.
2. Click **Add**.
3. Name the environment (e.g., `Local Testing`).
4. Add the following variables:

| Variable      | Initial Value            | Current Value            |
|---------------|--------------------------|--------------------------|
| `FASTAPI_URL` | `http://localhost:8000`  | `http://localhost:8000`  |
| `API_KEY`     | `your-app-api-key`       | `your-app-api-key`       |

> Note: This `API_KEY` refers to your **custom backend security key**, not the Groq API key.

5. Click **Save**.
6. Select the environment from the top-right dropdown.

---

## 🔄 4. Add and Configure Requests

### 🟢 A. `POST /query` – Execute SQL from Natural Language

1. In your collection, click **Add a Request**.
2. Name it: `Execute Natural Language Query`.
3. Set:
   - Method: `POST`
   - URL: `{{FASTAPI_URL}}/query`
4. Go to the **Headers** tab:
   - Key: `X-API-Key`
   - Value: `{{API_KEY}}`
5. Go to the **Body** tab:
   - Select `raw`
   - Choose `JSON`
   - Sample body:
     ```json
     {
       "query": "show me all female customer from mumbai",
       "case_sensitive": false
     }
     ```
6. Save the request.

### 🟡 B. `GET /health` – Health Check

1. Add another request to the same collection.
2. Name it: `Health Check`.
3. Method: `GET`
4. URL: `{{FASTAPI_URL}}/health`
5. Headers:
   - Key: `X-API-Key`
   - Value: `{{API_KEY}}`
6. Save the request.

---

## ▶️ 5. Run and Test

- Select your environment from the top-right dropdown.
- Click on any request and press **Send**.
- View the response data and status codes to verify behavior.

---

## ✅ Notes

- `API_KEY` is for your backend authentication and is validated using the `X-API-Key` header.
- `GROQ_API_KEY` is used **internally by the backend** and should not be exposed in Postman.
- Always ensure the backend server is running locally on `http://localhost:8000` or change `FASTAPI_URL` accordingly.

---

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
├── Screenshots          # screenshot of working 
    
```

## Compliance with Requirements

This implementation fully meets the problem statement requirements:

- ✅ **Tech Stack**: FastAPI backend, database integration, Groq LLM
- ✅ **Database Schema**: Exact schema with customer_id, name, gender, location
- ✅ **Functionality**: Natural language → LLM → SQL → Results → Display
- ✅ **Bonus Features**: Logging, error handling, environment variables, security
- ✅ **Deliverables**: All code, documentation, and setup instructions provided
