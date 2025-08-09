import json
import os

# Define the path to the JSON file relative to the current script's location
# This makes the path robust, regardless of where you run the app from.
DATA_FILE = os.path.join(os.path.dirname(__file__), 'sample_data.json')

def load_case_data_from_file():
    """Loads the case data from the local JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # This provides a clear error if the JSON file is missing.
        raise Exception(f"Error: The data file was not found at {DATA_FILE}")
    except json.JSONDecodeError:
        # This helps debug issues with the JSON file's format.
        raise Exception(f"Error: Could not decode the JSON from {DATA_FILE}. Check for syntax errors.")

def fetch_case_data(case_type, case_number, filing_year):
    """
    Searches for case data in the local JSON file instead of scraping a website.

    Args:
        case_type (str): The type of the case to search for.
        case_number (str): The case number to search for.
        filing_year (str): The filing year to search for.

    Returns:
        dict: A dictionary containing the details of the found case.

    Raises:
        Exception: If the case is not found in the local data file.
    """
    # Load the entire dataset from our JSON file.
    all_cases = load_case_data_from_file()

    # Search for a matching case.
    # We compare the form inputs (case-insensitively) with the data in the file.
    for case in all_cases:
        if (case['case_type'].lower() == case_type.lower() and
            case['case_number'] == case_number and
            case['filing_year'] == filing_year):
            
            # If a match is found, return the 'details' object for that case.
            return case['details']

    # If the loop completes without finding a match, raise an exception.
    raise Exception("Case not found in the local database. Please check the input details.")

