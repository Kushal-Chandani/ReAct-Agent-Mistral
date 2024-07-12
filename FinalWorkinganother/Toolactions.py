import sqlite3
from langchain.agents import tool
import json

############################################################################################

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

############################################################################################

@tool
def transfer_money(tool_input: str):
    """Transfers money from one person to another."""

    # Parse the JSON input
    try:
        data = json.loads(tool_input)

        # Handle different variations of sender and receiver keys
        sender_keys = ["from", "sender", "payer"]
        receiver_keys = ["to", "receiver", "recipient", "payee"]

        sender = next((data[key] for key in sender_keys if key in data), None)
        receiver = next((data[key] for key in receiver_keys if key in data), None)
        amount = float(data["amount"])

        if sender is None or receiver is None:
            raise KeyError("Missing sender or receiver information.")

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return f"Invalid input: {e}"

    # Request confirmation from the user
    confirmation = input(f"Do you want to transfer {amount} from {sender} to {receiver}? Type 'confirm' to proceed: ")

    if confirmation.lower() != 'confirm':
        return {"status": "cancelled", "message": "Transaction cancelled by user."}
    
    # Connect to the database
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    try:
        # Start a transaction
        conn.execute('BEGIN TRANSACTION')

        # Check sender's balance
        cursor.execute("SELECT Balance FROM customers WHERE Surname = ?", (sender,))
        sender_balance = cursor.fetchone()
        if not sender_balance:
            raise ValueError("Sender account not found.")
        sender_balance = sender_balance[0]

        # Check receiver's balance
        cursor.execute("SELECT Balance FROM customers WHERE Surname = ?", (receiver,))
        receiver_balance = cursor.fetchone()
        if not receiver_balance:
            raise ValueError("Receiver account not found.")
        receiver_balance = receiver_balance[0]

        # Check if sender has enough balance
        if sender_balance < amount:
            raise ValueError("Insufficient balance.")

        # Perform the transfer
        new_sender_balance = sender_balance - amount
        new_receiver_balance = receiver_balance + amount

        cursor.execute("UPDATE customers SET Balance = ? WHERE Surname = ?", (new_sender_balance, sender))
        cursor.execute("UPDATE customers SET Balance = ? WHERE Surname = ?", (new_receiver_balance, receiver))

        # Commit the transaction
        conn.commit()

        result = {
            "status": "success",
            "message": f"Transfer successful. New balance: {sender} = {new_sender_balance}, {receiver} = {new_receiver_balance}"
        }

    except Exception as e:
        # Rollback the transaction in case of error
        conn.rollback()
        result = {"status": "error", "message": str(e)}

    finally:
        conn.close()

    return result
