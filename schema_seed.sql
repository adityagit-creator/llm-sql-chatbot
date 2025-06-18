CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY IDENTITY(1,1),
    name TEXT NOT NULL,
    gender TEXT,
    location TEXT
);

INSERT INTO customers (name, gender, location) VALUES
    ('John Doe', 'Male', 'New York'),
    ('Jane Smith', 'Female', 'Mumbai'),
    ('Alice Johnson', 'Female', 'London'),
    ('Bob Brown', 'Male', 'Mumbai'),
    ('Charlie Davis', 'Male', 'Paris'),
    ('Diana Evans', 'Female', 'Mumbai'),
    ('Eve Wilson', 'Female', 'Tokyo');