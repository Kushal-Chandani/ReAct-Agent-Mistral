# from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from database_query_tool import query_database
from transfertoo import transfer_money
from react_template import get_react_prompt_template
from langchain_community.llms import Ollama

# Load environment variables
# load_dotenv()

# Choose the LLM to use
llm = Ollama(model="mistral")

# Set my message
query = "Transfer $200 from Rania's account to Hill's account"

# Set the tools
tools = [transfer_money]

# Get the react prompt template
prompt_template = get_react_prompt_template()

# Construct the ReAct agent
agent = create_react_agent(llm, tools, prompt_template)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Execute the query
response = agent_executor.invoke({"input": query})
print(response)




