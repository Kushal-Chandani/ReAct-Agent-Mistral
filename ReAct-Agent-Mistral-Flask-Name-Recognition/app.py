# from flask import Flask, request, render_template
# from langchain.agents import AgentExecutor, create_react_agent
# from react_template import get_react_prompt_template
# from langchain_community.llms import Ollama
# from Toolactions import transfer_money, get_balance

# app = Flask(__name__)

# # Choose the LLM to use
# llm = Ollama(model="mistral")

# # Set the tools
# tools = [transfer_money, get_balance]

# # Get the react prompt template
# prompt_template = get_react_prompt_template()

# # Construct the ReAct agent
# agent = create_react_agent(llm, tools, prompt_template)

# # Create an agent executor by passing in the agent and tools
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/query', methods=['POST'])
# def query():
#     user_query = request.form['query']
#     response = agent_executor.invoke({"input": user_query})
#     if isinstance(response, dict) and response.get("status") == "cancelled":
#         result = response["message"]
#     else:
#         result = response.get('output', 'No response received')
#     return render_template('index.html', query=user_query, result=result)

# if __name__ == '__main__':
#     app.run(debug=True)

################################################################################

################################################################################

#React Agent with Flask sent on the group

# from flask import Flask, request, render_template, jsonify
# from langchain.agents import AgentExecutor, create_react_agent
# from react_template import get_react_prompt_template
# from langchain_community.llms import Ollama
# from Toolactions import transfer_money, get_balance

# app = Flask(__name__)

# # Choose the LLM to use
# llm = Ollama(model="mistral")

# # Set the tools
# tools = [transfer_money, get_balance]

# # Get the react prompt template
# prompt_template = get_react_prompt_template()

# # Construct the ReAct agent
# agent = create_react_agent(llm, tools, prompt_template)

# # Create an agent executor by passing in the agent and tools
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/query', methods=['POST'])
# def query():
#     user_query = request.form['query']
#     response = agent_executor.invoke({"input": user_query})
#     if isinstance(response, dict) and response.get("status") == "confirm":
#         return jsonify({"status": "confirm", "message": response["message"], "data": response["data"], "query": user_query})
#     else:
#         result = response.get('output', 'No response received')
#         return jsonify({"status": "success", "query": user_query, "result": result})

# @app.route('/confirm', methods=['POST'])
# def confirm():
#     data = {
#         "sender": request.form['sender'],
#         "receiver": request.form['receiver'],
#         "amount": float(request.form['amount']),
#         "confirmation": "confirm"
#     }
#     response = transfer_money(data)
#     return jsonify({"status": response["status"], "message": response["message"], "query": request.form['query']})

# if __name__ == '__main__':
#     app.run(debug=True)

################################################################################

################################################################################

from flask import Flask, request, render_template, jsonify, session
from langchain.agents import AgentExecutor, create_react_agent
from react_template import get_react_prompt_template
from langchain_community.llms import Ollama
from Toolactions import transfer_money, get_balance
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Choose the LLM to use
llm = Ollama(model="mistral")

# Set the tools
tools = [transfer_money, get_balance]

# Get the react prompt template
prompt_template = get_react_prompt_template()

# Construct the ReAct agent
agent = create_react_agent(llm, tools, prompt_template)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('chatbot.db')
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_name', methods=['POST'])
def check_name():
    name = request.form['name']
    result = query_db('SELECT surname FROM customers WHERE surname = ?', [name], one=True)
    if result:
        session['username'] = name
        return jsonify({'status': 'found'})
    else:
        return jsonify({'status': 'not found'})

@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['query']
    username = session.get('username')

    if not username:
        return jsonify({"status": "error", "result": "User not logged in."})

    if f"User: {username}" not in user_query:
        return jsonify({"status": "error", "result": "You can only query your own data."})

    response = agent_executor.invoke({"input": user_query})
    if isinstance(response, dict) and response.get("status") == "confirm":
        return jsonify({"status": "confirm", "message": response["message"], "data": response["data"], "query": user_query})
    else:
        result = response.get('output', 'No response received')
        return jsonify({"status": "success", "query": user_query, "result": result})

@app.route('/confirm', methods=['POST'])
def confirm():
    data = {
        "sender": request.form['sender'],
        "receiver": request.form['receiver'],
        "amount": float(request.form['amount']),
        "confirmation": "confirm"
    }
    response = transfer_money(data)
    return jsonify({"status": response["status"], "message": response["message"], "query": request.form['query']})

if __name__ == '__main__':
    app.run(debug=True)

