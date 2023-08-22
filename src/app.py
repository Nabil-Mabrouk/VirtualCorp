import os
import openai
from dotenv import load_dotenv

# Access the secret key
load_dotenv()
DEBUG = (os.getenv("DEBUG") == "TRUE") or False
openai.api_key = os.getenv("OPENAI_API_KEY")
MAX_WORDS= os.getenv("MAX_WORDS")

from agent import Agent, AgentType
from contract import Contract
from pipeline import Pipeline

from logger_config import logger
from model import HumanModel, GPTModel
import prompts as pts

def start():

    logger.info("WELCOM TO VirtualCORP - version 1.0 - 08/2023\n")

    # Create an instance of the HumanModel
    model1 = HumanModel()
    agent1=Agent(name="Client", model=model1, template=pts.human_prompt)

    # Virtual agent language model
    model_name= "gpt-3.5-turbo"

    # Step 1 : business idea validation process
    ## Create business idea validator agent
    model2=GPTModel(model_name)
    agent2=Agent(name="Welcome agent", model=model2, template=pts.agent2_prompt)

    ## Create the smart contract for business validation step
    contract_model1=GPTModel(model_name)
    contract1=Contract("Business Validation", agent1=agent1, agent2=agent2, model=contract_model1, template=pts.contract1_prompt)

    pipeline = Pipeline(name="VirtualCorp", contracts=[contract1])
    






def start(user_name, initial_input):

    # Initialization of the pipeline
    pipe = Pipeline(name="VirtualCORP")

    # Step 1: Business idea validation
    # --- Agent 1: Human
    human = Agent(name=user_name, type=AgentType.HUMAN)

    # --- Agent 2: Virtual agent
    welcomeAgent = Agent(name = "Welcome Agent", type=AgentType.VIRTUAL)
    
    # Agent 1 prompt template (add here any rule that you want the Human agent to comply with)
    humanTemplate = """
    You are a Human. You will be interacting with a virtual agent. You must propose a legal busines idea.
    You are allowed to suggest modification of the rephrased business idea
    If you business idea or suggested modification do not comply with legal, ethical or any other rule you will recieve a notification and an explanation
    In this case you must modify your business idea and submit a compliant business idea
    Termination condition: your interaction with the virtual agent ends when you express your agreement with the rephrased idea without any new suggestion of modifications
    ------------
    The virtual agent rephrasing : {input}
    Compliance check result : {status}
    Compliance check explanation: {reasons}
    """
    human.setTemplate(humanTemplate)
    welcomeTemplate = """
    You are a virtual agent and you will recieve a business idea from a human.
    You must rephrase the business idea in less than 200 words. 
    You will submit your rephrased idea to the human for validation.
    Your answer will be checked to make sure that it is compliant with legal, ethical or any other rule.
    If your rephrased idea is not compliant you will recieve a notification saying that your answer is NOT COMPLIANT and an explanation
    In this case you must rephrase your answer to make it compliant
    The Human can also suggest modification even if your answer is compliant
    You must evaluate if these modifications are relevant or not and rephrase the business idea accordingly
    You must always answer with the rephrased business idea.
    You are not allowed to provide any explanation or any comment. Only answer with you rephrased business idea.
    ---------------------------
    Human message : {input}
    ---------------------------
    The result of the compliance check: {status}
    ---------------------------
    The explanations of the compliance result: {reasons}
    ---------------------------
    """
    welcomeAgent.setTemplate(welcomeTemplate)

    ## Create the contract
    initialContract = Contract(name='Welcome desk', agent1=human, agent2=welcomeAgent)

    ## register the contract
    pipe.add(initialContract)
    
    ## Start the pipeline

    pipe.execute(initial_input)
    
    ## Log the pipeline
    for entry in pipe.pipeline:
        print(entry)
    
    
if __name__ == '__main__':

    # Wecome message:
    print(" -------------------------------------------------------------------------------------------------")
    print("Welcome at VirtualCORP. We automate compliant business creation from you initial")
    print("seed idea to the final package including a business plan a detailed business process")
    print("and a documented code source. \n")

    print("Compliance is our DNA. Every single step or interaction with out agent is checked")
    print("for compliance with ethical and legal rules and domain specific best practices")
    print("The result is perfectly compliant product that allows you to start you compliant business in few clicks.")
    print(" -------------------------------------------------------------------------------------------------")

    user_name= input("VirtualCORP: Please enter your name:")
    initial_input = input("VirtualCORP: Please enter your business idea:")
    start(user_name, initial_input)