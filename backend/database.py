import sqlite3
import json
from datetime import datetime

DB_NAME = 'search_log.db'

def init_db():
    """Creates the database and table if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create table to log searches
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT NOT NULL,
            case_number TEXT NOT NULL,
            filing_year TEXT NOT NULL,
            scraped_data_json TEXT,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def log_search(case_type, case_number, filing_year, result_data):
    """Logs a single search event to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO search_history (case_type, case_number, filing_year, scraped_data_json, timestamp) VALUES (?, ?, ?, ?, ?)",
        (
            case_type,
            case_number,
            filing_year,
            json.dumps(result_data), # Store the full result as a JSON string
            datetime.now().isoformat()
        )
    )
    conn.commit()
    conn.close()
    print(f"Successfully logged search for {case_type}/{case_number}/{filing_year}")