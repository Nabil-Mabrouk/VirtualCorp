human_prompt = """ You have to provide a legal business idea. You business idea should be related to sport. 
Your busines idea will be rephrased by a virtual agent. If the rephrased business idea is OK for you you must return {{terminated}}.
You are allowed to suggest modifications otherwise
-----
- VirtualCorp message: <MESSAGE>
- your last message: <LAST MESSAGE>
-----
"""

agent_prompt="""You will be provided by a message from another agent. You role is to rephrase a business idea and return back your rephrased version.
The message that you will recieve can be either the business idea or a comment on your previous answer. In this case you will be provided also with you last answer
-----
Message of the agent: <MESSAGE>
your last rephrased business idea: <LAST MESSAGE>
-----
Your answer must be only with your rephrased business idea.
If the message containes {{terminated}} you must return your last business idea and nothing else.
"""
extract_rules_template="""
Task Description: Your task is to extract and list the specific constraints that apply to each agent based 
solely on their provided instructions. Avoid inventing any rules not mentioned in their respective instructions. 
The focus should be on extracting compliance rules for each agent, excluding any related to termination conditions.
For example:
Q: extract the constrains that agent1 must comply with based on the following instructions:
- Instruction of agent 1: Provide a legal busines idea. You are allowed to revise your idea. You will recieve a proposition rephrasing your business idea. You are allowed to suggest modification
A: 
- Agent 1 must provide a legal idea
- Agent 1 is allowed to submit suggestions to modify the rephrased busines idea

Q: extract constrains for agent <EXTRACT RULES FOR AGENT> based on the following instructions
Agent 1 name: <FIRST AGENT NAME> 
Instructions for Agent 1: <FIRST AGENT INSTRUCTIONS>

Agent 2 name: <SECOND AGENT NAME> 
Instructions for Agent 1: <SECOND AGENT INSTRUCTIONS>

Please provide your answer in the form of a bullet-pointed list of rules. Do not include any additional information.
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

compliance_check_prompt = """ You will be provided with a message generated by an agent and a set of compliance rules.
Your role is to check if the message is compliant with the provided rules.
Your answer should be either "COMPLIANT" or "NON COMPLIANT". If the message is non compliant you must provide 
a step by step and very detailed explanation of the reasons of the non compliance and suggets how to make the message compliant.
Refer only to the provided rules.
---------
Sender Agent name: <AGENT NAME>
Sent message: <MESSAGE>
Compliance rules: <RULES>
-----
If the agent message is compliant with hte rule you must answer only with the word: COMPLIANT and nothing else
"""
