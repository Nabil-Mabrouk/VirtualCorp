import os
import openai
from dotenv import load_dotenv
# Access the secret key
load_dotenv()
DEBUG = (os.getenv("DEBUG") == "TRUE") or False
openai.api_key = os.getenv("OPENAI_API_KEY")

from agent import Agent, AgentType
from contract import Contract
from pipeline import Pipeline


def start():
    # Initialization
    pipe = Pipeline(name="VirtualCORP")
    human = Agent(name="Human", type=AgentType.HUMAN)
    welcomeAgent = Agent(name = "Welcome Agent", type=AgentType.VIRTUAL)
    
    # start the pipeline
    # step 1: validate business idea
    humanTemplate = """
    You will be interacting with a virtual agent. You have to propose a legal busines idea.
    The agent will rephrase your idea.
    The contract will tell you if your message is compliant or not.
    If the decision of the contract is not compliant, please, modify your answer.
    If the answer of the virtual agent is plausible and you agree with the rephrasing, answer "I agree".
    If you do not agree, please, suggest a modification.
    The virtual agent rephrasing will appear here: {input}
    The contract decision will appear here: {status}
    The contract reasons will appear here: {reasons}
    """
    human.setTemplate(humanTemplate)
    welcomeTemplate = """
    You will recieve a business idea from a human.
    You must rephrase the business idea in less than 200 words. 
    You will submit you rephrased idea to the human for validation.
    The contract will tell you if your answer is compliant or not and will give the reasons of its decision.
    If the decision of the contract is not compliant, please, suggest another answer.
    You need to take into account the reasons of the contract to modify your answer.
    You are done once the human express his agreement.
    The user agent phrase is : {input}
    The contract decision will appear here: {status}
    The contract reasons will appear here: {reasons}
    """
    welcomeAgent.setTemplate(welcomeTemplate)

    ## Create the contract
    initialContract = Contract(name='Welcome desk', agent1=human, agent2=welcomeAgent)

    ## register the contract
    pipe.add(initialContract)
    
    ## Start the pipeline
    print("Welcome at VirtualCORP")
    initial_input = "Please what is your business idea ?"
    pipe.execute(initial_input)
    
    ## Log the pipeline
    for entry in pipe.pipeline:
        print(entry)
    
    
if __name__ == '__main__':
    start()