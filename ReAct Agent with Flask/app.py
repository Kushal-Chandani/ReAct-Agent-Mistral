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

############################################################################################3

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
#     if isinstance(response, dict) and response.get("status") == "cancelled":
#         result = response["message"]
#     else:
#         result = response.get('output', 'No response received')
    
#     if "transfer" in user_query.lower():
#         return jsonify({"confirmation_needed": True, "query": user_query, "result": result})
#     else:
#         return render_template('index.html', query=user_query, result=result)

# @app.route('/confirm_transfer', methods=['POST'])
# def confirm_transfer():
#     user_query = request.form['query']
#     response = agent_executor.invoke({"input": user_query})
#     if isinstance(response, dict) and response.get("status") == "cancelled":
#         result = response["message"]
#     else:
#         result = response.get('output', 'No response received')
    
#     return render_template('index.html', query=user_query, result=result)

# if __name__ == '__main__':
#     app.run(debug=True)


################################################################################3

from flask import Flask, request, render_template, jsonify
from langchain.agents import AgentExecutor, create_react_agent
from react_template import get_react_prompt_template
from langchain_community.llms import Ollama
from Toolactions import transfer_money, get_balance

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_query = request.form['query']
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
