# # from dotenv import load_dotenv
# from langchain.agents import AgentExecutor, create_react_agent
# from get_balance_func import get_balance
# from transfer_mon import transfer_money
# from react_template import get_react_prompt_template
# from transaction import get_user_transactions
# from langchain_community.llms import Ollama

# # Load environment variables
# # load_dotenv()

# # Choose the LLM to use
# llm = Ollama(model="mistral")

# # Set my message
# # query = "Rania wants to transfer 100 to Hill"
# # query = "what is the balance of Rania?"
# # query = "Give Hill's latest transaction"
# query = input("Please enter your query: ") 

# # Set the tools
# tools = [transfer_money, get_balance, get_user_transactions]

# # Get the react prompt template
# prompt_template = get_react_prompt_template()

# # Construct the ReAct agent
# agent = create_react_agent(llm, tools, prompt_template)

# # Create an agent executor by passing in the agent and tools
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# # Execute the query
# response = agent_executor.invoke({"input": query})
# print(response)

# from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from get_balance_func import get_balance
from transfer_mon import transfer_money
from react_template import get_react_prompt_template
from langchain_community.llms import Ollama

# Load environment variables if needed
# from dotenv import load_dotenv
# load_dotenv()

# Choose the LLM to use
llm = Ollama(model="mistral")

# Set the tools
tools = [transfer_money, get_balance]

# Get the react prompt template
prompt_template = get_react_prompt_template()

# Construct the ReAct agent
agent = create_react_agent(llm, tools, prompt_template)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Loop to keep taking user input until they decide to stop
while True:
    query = input("Please enter your query (or type 'exit' to quit): ")
    if query.lower() == 'exit':
        break
    response = agent_executor.invoke({"input": query})
    print(response)

