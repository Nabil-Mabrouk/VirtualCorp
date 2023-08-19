from agent import Agent, AgentType
from contract import Contract
from pipeline import Pipeline


def start():
    pipe = Pipeline()
    # Initialization
    print("Welcome at VirtualCORP")
    user_input = (input("Please enter your business idea : ")
                  or "Launch an ecommerce business to trade 3d printed parts")
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
    initialContract = Contract(agent1=human, agent2=welcomeAgent)

    ## register the contract
    pipe.add(initialContract)
    
    pipe.execute(user_input)
    
    for entry in pipe.pipeline:
        print(entry)
    
    
if __name__ == '__main__':
    start()