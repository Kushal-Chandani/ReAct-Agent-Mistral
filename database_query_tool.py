import sqlite3
from langchain.agents import tool

@tool
def query_database(name: str):
    """Retrieves the account balance for the specified person."""

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


# Create an instance of the tool
query_db_tool = query_database

# Use the invoke method
result = query_db_tool.invoke("Romeo")
print(result)
