import sqlite3
from langchain.agents import tool
import json

@tool
def get_balance(tool_input: str):
    """Retrieves the account balance for the specified person."""

    # Parse the JSON input
    try:
        data = json.loads(tool_input)
        name = data["person"]
    except (json.JSONDecodeError, KeyError) as e:
        name = tool_input
        # return f"Invalid input: {e}"

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

@tool
def transfer_money(tool_input: str):
    """Transfers money from one person to another."""

    # Parse the JSON input
    try:
        data = json.loads(tool_input)
        if "from" in data.keys():
            sender = data["from"]
            receiver = data["to"]
        else:
            sender = data["sender"]
            receiver = data["receiver"]
        amount = float(data["amount"])
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

from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama
from react_template import get_react_prompt_template

# Load environment variables
# load_dotenv()

# Choose the LLM to use
llm = Ollama(model="mistral")

# Set my message
# query = "Rania wants to transfer 100 to Hill"
# query = "what is the balance of Rania?"
# query = "Give Hill's latest transaction"
query = input("Please enter your query: ") 

# Set the tools
tools = [transfer_money, get_balance, get_user_transactions]

# Get the react prompt template
prompt_template = get_react_prompt_template()

# Construct the ReAct agent
agent = create_react_agent(llm, tools, get_react_prompt_template())

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Execute the query
response = agent_executor.invoke({"input": query})
print(response)