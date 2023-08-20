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
    You will be interacting with a virtual agent. You have to propose a legal busines idea. the agent will rephrase your idea.
    If you agree with the rephrasing type "I agree". If not suggest a modification.
    The virtual agent rephrasing will appear here: {input}
    """
    human.setTemplate(humanTemplate)
    welcomeTemplate = """
    You will recieve a business idea from a human. You must rephrase the business idea in less than 200 words. 
    You will submit you rephrased idea to the human for validation. You are done once the human express his agreement.
    The user agent phrase is : {input}
    """
    welcomeAgent.setTemplate(welcomeTemplate)

    ## Create the contract
    initialContract = Contract(name='Welcome desk', agent1=human, agent2=welcomeAgent)

    ## register the contract
    pipe.add(initialContract)
    
    ## Start the pipeline
    print("Welcome at VirtualCORP")
    initial_input = "Please enter your business idea : "
    pipe.execute(initial_input)
    
    ## Log the pipeline
    for entry in pipe.pipeline:
        print(entry)
    
    
if __name__ == '__main__':
    start()