# from langchain_core.prompts import PromptTemplate

# def get_react_prompt_template():
#     # Get the react prompt template
#     return PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

# {tools}

# Use the following format:

# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question

# Begin!

# Question: {input}
# Thought: {agent_scratchpad}
# """)

from langchain_core.prompts import PromptTemplate

def get_react_prompt_template():
    # Get the react prompt template
    return PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: I need to retrieve the account balance for the specified person.
Action: query_database
Action Input: The name of the person whose account balance is needed
Observation: The result of the database query
Thought: I now know the final answer
Final Answer: the account balance of the specified person
                                        
# Question: {input}
# Thought: {agent_scratchpad}
""")
