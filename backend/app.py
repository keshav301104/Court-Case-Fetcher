from flask import Flask, render_template, request, jsonify
from .scrapper import fetch_case_data
import json

# This is the new database setup part
import sqlite3

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

def init_db():
    """Initializes the SQLite database and creates the table if it doesn't exist."""
    conn = sqlite3.connect('queries.db')
    cursor = conn.cursor()
    # Create a table to log every search query and its result
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT NOT NULL,
            case_number TEXT NOT NULL,
            filing_year TEXT NOT NULL,
            result_found BOOLEAN NOT NULL,
            raw_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_search(case_type, case_number, filing_year, result):
    """Logs the search details and the result into the SQLite database."""
    conn = sqlite3.connect('queries.db')
    cursor = conn.cursor()
    
    result_found = result is not None
    # Store the result as a JSON string
    raw_response = json.dumps(result) if result_found else None
    
    cursor.execute('''
        INSERT INTO search_log (case_type, case_number, filing_year, result_found, raw_response)
        VALUES (?, ?, ?, ?, ?)
    ''', (case_type, case_number, filing_year, result_found, raw_response))
    
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    template_data = {}
    if request.method == "POST":
        case_type = request.form.get("case_type")
        case_number = request.form.get("case_number")
        filing_year = request.form.get("filing_year")
        
        # Keep form data to repopulate fields on error
        template_data['form_data'] = request.form

        try:
            if not all([case_type, case_number, filing_year]):
                raise Exception("All fields are required.")
            
            # Call the simplified scraper function
            result = fetch_case_data(case_type, case_number, filing_year)
            template_data['result'] = result
            
            # Log the successful search to the database
            log_search(case_type, case_number, filing_year, result)

        except Exception as e:
            # If there's an error (e.g., case not found), show it
            template_data['error'] = str(e)
            # Log the failed search attempt
            log_search(case_type, case_number, filing_year, None)

    return render_template("index.html", **template_data)

if __name__ == "__main__":
    # Initialize the database when the app starts
    init_db()
    app.run(debug=True)
