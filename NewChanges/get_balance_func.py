import sqlite3
from langchain.agents import tool
import json

@tool
def get_balance(tool_input: str):
    """Retrieves the account balance for the specified person."""

    # Parse the JSON input
    try:
        data = json.loads(tool_input)

        # Handle different variations of name keys
        name_keys = ["person", "name"]
        name = next((data[key] for key in name_keys if key in data), None)

        if name is None:
            raise KeyError("Missing name information.")

    except (json.JSONDecodeError, KeyError) as e:
        name = tool_input

    # Connect to the database
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT Balance FROM customers WHERE Surname = ?", (name,))
        result = cursor.fetchone()
        if result:
            result = result[0]
        else:
            result = "Account not found."
    except Exception as e:
        result = str(e)
    
    conn.close()
    return result

# # Create an instance of the tool
# query_db_tool = query_database

# # Use the invoke method with a JSON string
# result = query_db_tool.invoke(json.dumps({"name": "Romeo"}))
# print(result)
