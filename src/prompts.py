human_prompt = """you have to provide a legal business idea. You business idea should be related to sport. If you agree with the rephrased you should return {{TERMINATED}} to end the interaction"""

agent_prompt="""You will be provided by a business idea. You role is to rephrase it
"""
extract_rules_template="""You will be provided with the prompt of two agents. Agent 1 is named <FIRST AGENT NAME>. Agent 2 is named <SECOND AGENT NAME>.
Each agent recieved a set of instructions. You role is to extract from these instructions and only from these instructions
the rules that agent <EXTRACT RULES FOR AGENT> must complu with. Don't invent rules that are not mentioned in the instructions of the agents.
 ------------------------------------
 First agent instructions are: <FIRST AGENT INSTRUCTIONS>
 ------------------------------------
 Second agent instructions are: <SECOND AGENT INSTRUCTIONS>
 ------------------------------------
Your answer should be limited to the rules and constrains that agent <EXTRACT RULES FOR AGENT> must comply with for his answer to be compliant 
Ignore any rule related to termination condition
Return your answer as a bullet list of rules. DO not add anythink else to your answer:
"""

extract_termination_keywords="""You will be provided with the the instructions of two agents. Agent 1 is named <FIRST AGENT NAME>. Agent 2 is named <SECOND AGENT NAME>.
Each agent recieved a set of instructions. They will collaborate to achieve a mission. The mission ends once on of the agents return a termination keyword. 
You role is to extract this termination keyword from the instructions that each agent recieved.
 ------------------------------------
 Agent1 instructions: <FIRST AGENT INSTRUCTIONS>
 ------------------------------------
  ------------------------------------
 Agent2 instructions: <SECOND AGENT INSTRUCTIONS>
 ------------------------------------
Your answer should contain only the termination keywords
Return your answer as a bullet list of keywords. DO not add anythink else to your answer:
"""

