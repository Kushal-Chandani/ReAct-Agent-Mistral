import sqlite3
from langchain.agents import tool
import json

@tool
def get_user_transactions(tool_input: str):
    """Retrieves transactions for the specified sender."""

    # Parse the JSON input
    try:
        data = json.loads(tool_input)
        sender_surname = data["name"]
    except (json.JSONDecodeError, KeyError) as e:
        return f"Invalid input: {e}"

    # Connect to the database
    conn = sqlite3.connect('chatbot_tranc.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT transaction_id, sender_surname, receiver_surname, amount, transaction_date FROM transactions WHERE sender_surname = ?", (sender_surname,))
        result = cursor.fetchall()
        if result:
            result = [dict(transaction_id=row[0], sender_surname=row[1], receiver_surname=row[2], amount=row[3], date=row[4]) for row in result]
        else:
            result = "No transactions found."
    except Exception as e:
        result = str(e)
    
    conn.close()
    return result

# # Create an instance of the tool
# get_user_transactions_tool = get_user_transactions

# # Use the invoke method with a JSON string
# result = get_user_transactions_tool.invoke(json.dumps({"sender_surname": "Hill"}))
# print(result)
