# import sqlite3
# from langchain.agents import tool
# import json

# @tool
# def transfer_money(tool_input: str):
#     """Transfers money from one person to another."""

#     # Parse the JSON input
#     try:
#         data = json.loads(tool_input)
#         if "from" in data.keys():
#             sender = data["from"]
#             receiver = data["to"]
#         else:
#             sender = data["sender"]
#             receiver = data["receiver"]
#         amount = float(data["amount"])
#     except (json.JSONDecodeError, KeyError, ValueError) as e:
#         return f"Invalid input: {e}"

#     # Connect to the database
#     conn = sqlite3.connect('chatbot.db')
#     cursor = conn.cursor()

#     try:
#         # Start a transaction
#         conn.execute('BEGIN TRANSACTION')

#         # Check sender's balance
#         cursor.execute("SELECT Balance FROM customers WHERE Surname = ?", (sender,))
#         sender_balance = cursor.fetchone()
#         if not sender_balance:
#             raise ValueError("Sender account not found.")
#         sender_balance = sender_balance[0]

#         # Check receiver's balance
#         cursor.execute("SELECT Balance FROM customers WHERE Surname = ?", (receiver,))
#         receiver_balance = cursor.fetchone()
#         if not receiver_balance:
#             raise ValueError("Receiver account not found.")
#         receiver_balance = receiver_balance[0]

#         # Check if sender has enough balance
#         if sender_balance < amount:
#             raise ValueError("Insufficient balance.")

#         # Perform the transfer
#         new_sender_balance = sender_balance - amount
#         new_receiver_balance = receiver_balance + amount

#         cursor.execute("UPDATE customers SET Balance = ? WHERE Surname = ?", (new_sender_balance, sender))
#         cursor.execute("UPDATE customers SET Balance = ? WHERE Surname = ?", (new_receiver_balance, receiver))

#         # Commit the transaction
#         conn.commit()

#         result = f"Transfer successful. New balance: {sender} = {new_sender_balance}, {receiver} = {new_receiver_balance}"

#     except Exception as e:
#         # Rollback the transaction in case of error
#         conn.rollback()
#         result = str(e)

#     finally:
#         conn.close()

#     return result

import sqlite3
from langchain.agents import tool
import json

@tool
def transfer_money(tool_input: str):
    """Transfers money from one person to another."""

    # Parse the JSON input
    try:
        data = json.loads(tool_input)

        # Handle different variations of sender and receiver keys
        sender_keys = ["from", "sender"]
        receiver_keys = ["to", "receiver", "recipient"]

        sender = next((data[key] for key in sender_keys if key in data), None)
        receiver = next((data[key] for key in receiver_keys if key in data), None)
        amount = float(data["amount"])

        if sender is None or receiver is None:
            raise KeyError("Missing sender or receiver information.")

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return f"Invalid input: {e}"

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

        result = f"Transfer successful. New balance: {sender} = {new_sender_balance}, {receiver} = {new_receiver_balance}"

    except Exception as e:
        # Rollback the transaction in case of error
        conn.rollback()
        result = str(e)

    finally:
        conn.close()

    return result

