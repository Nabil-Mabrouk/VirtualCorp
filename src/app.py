
import agent
import contract

if __name__ == '__main__':

    pipeline = []

    # Initialization
    print("Welcome at VirtualCORP \n")
    user_input = input("Please enter your business idea : ")

    # start

    # step 1: validate business idea
    human = agent.Agent(name="Human", type = agent.HUMAN)
    humanTemplate="""   You will be interacting with a virtual agent. You have to propose a legal busines idea. the agent will rephrase your idea.
    If you agree with the rephrasing type "I agree". If not suggest a modification.
    """
    human.setTemplate(humanTemplate)
    welcomeAgent = agent.Agent(name = "Welcome Agent", type = agent.VIRTUAL)
    agent1Template=""" You will recieve a business idea from a human. You must rephrase the business idea in less than 200 words. 
    You will submit you rephrased idea to the human for validation. You are done once the human express his agreement.
    """
    welcomeAgent.setTemplate(agent1Template)

    ## Create the contract
    contract1 = contract.Contract(agent1=human, agent2 = welcomeAgent)

    ## register the contract
    pipline.append(contract1)


    #step 2: etc ..
