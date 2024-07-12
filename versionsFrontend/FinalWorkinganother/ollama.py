from langchain.agents import AgentExecutor, create_react_agent
from react_template import get_react_prompt_template
from langchain_community.llms import Ollama
from Toolactions import transfer_money, get_balance

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
    if isinstance(response, dict) and response.get("status") == "cancelled":
        print(response["message"])
    else:
        print(response)