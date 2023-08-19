# bring openai api key
import os
import sys
from tabnanny import check
import openai
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.schema import HumanMessage

# Access the secret key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Contract():
    def __init__(self, agent1, agent2, llm=ChatOpenAI(temperature=0)):
        self.agent1 = agent1
        self.agent2 = agent2
        self.llm = llm
        self.rules = []
        self.initialize()
    
    def initialize(self):
        # prompt1 = self.agent1.getPrompt()
        # prompt2 = self.agent2.getPrompt()
        initPrompt = """
        The company VirtualCorp help business owners to find the best business idea for them.
        The field of operation is any B2C business related to eCommerce and merchandise trading.
        The agent {agent1} is a human and the agent {agent2} is a virtual agent.
        The agent {agent1} will propose a business idea and the agent {agent2} will rephrase it.
        The agent {agent1} will validate the rephrasing.
        And the agent {agent2} will validate the business idea if it fits VirtualCorp field of operation.
        Both agents should stick to the following rules:
        - The agent {agent1} should propose a business idea that fits VirtualCorp field of operation.
        - The agent {agent2} should rephrase the business idea in less than 200 words.
        - The agent {agent1} should validate the rephrasing.
        - The agent {agent2} should validate the business idea if it fits VirtualCorp field of operation.
        Extract all the rules each agent has to fullfill during their interaction.
        """
        systemPrompt = (SystemMessagePromptTemplate
                        .from_template(initPrompt)
                        .format(agent1=self.agent1.name, agent2=self.agent2.name))
        self.rules = self.parse(self.llm(HumanMessage(content=systemPrompt.content))) # syntax à revoir
    
    def check(self, message):
        answer = 1
        checkPrompt = """
        Check that this message: {message} respect all these rules : {rules}. You must answer TRUE if all
        the rules are respected or FALSE if at least one rule is not respected.
        """
        systemPrompt = (SystemMessagePromptTemplate
                        .from_template(checkPrompt)
                        .format(message=message, rules=self.rules))
        # à mettre dans un block try/except intelligent?    #syntax à revoir
        answer = self.parse(self.llm(HumanMessage(content=systemPrompt.content)))    
        return answer
    
    def parse(self, message):
        return message
    
    ## A compléter il faut une while loop and verif de la condition de terminaison
    def run(self, input):
        result = False
        while not result:
            output = self.agent1.getPrompt(input)
            result = self.check(output)
        
        result = False
        while not result:
            output = self.agent2.getPrompt(input)
            result = self.check(output)
            
        return output
            
                
    

