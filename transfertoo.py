import sqlite3
from langchain.agents import tool

@tool
def transfer_money(sender: str, receiver: str, amount: float):
    """Transfers money from one person to another."""

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

# Create an instance of the tool
# transfer_tool = transfer_money

# Create the input dictionary
# input_data = {
#     'sender': 'Romeo',
#     'receiver': 'Rania',
#     'amount': 500.0
# }

# Use the invoke method
# result = transfer_tool.invoke(input_data)
# print(result)
