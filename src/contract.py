# bring openai api key
import os
import sys
from tabnanny import check
import openai
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.schema import HumanMessage

from pydantic import BaseModel
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

# Access the secret key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ajouter un nom au contrat pour mieux l'identifier dans le log ou dans les print. Branch new --> [DONE]
class Contract():
    def __init__(self, name, agent1, agent2, llm=ChatOpenAI(temperature=0)):
        self.name = name
        self.agent1 = agent1
        self.agent2 = agent2
        self.llm = llm
        self.rules = self._initialize()
    
    # mon idée initiale est que le llm du contrat génère automatiquement les rules à partir des promptTemplates
    # des agents. Pourquoi? parce que les rules à respecter entre le contrat initial (human/agent) et le contrat (agent/agent) ne sont pas forcément les mêmes
    # l'agent a une mission de faire un certain nombre de choses, de produire un output dans un format particulier. Le contrat contôle que l'agent rempli bien 
    # la mission qui lui a été attribué
    # idem dans un agent HUMAN on peut imaginer un promptTemplate qui défini ce qui est attendu de l'Humain par l'agent avec qui il va interagir.
    # j'ai pensé aussi aux rules comme une liste de manière à identifier la rule qui n'a pas été respectée dans un contrat et d'avoir des messages du type:
    # contract name: Violation of rule [rule id] by agent [agent name]. Rule [Rule_id]: [rule_description]. [agent_output]: ....
    # on peut ultérieurement avec ça collecter progressivement des infos sur le type de rule avec lesquels les llm galèrent et fine-tuner de manière plus spécifique

    def _initialize(self):
        prompt1= self.agent1.getPromptTemplate()
        agent1=self.agent1.getName()

        prompt2= self.agent2.getPromptTemplate()
        agent2 = self.agent2.getName()

        response_schemas = [
              ResponseSchema(name="agent", description="Name of the agent"),
              ResponseSchema(name="rule", description="Rule or constrain that the agent must comply with")
              ]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        template = """
            The agent named {agent1} recieved the following prompt:
            Prompt: {prompt1}

            The agent named {agent2} recieved the following prompt
            Prompt: {prompt2}

            From these prompts extract the rules and constrain that each agent should comply with
            {format_instructions}
        """
        prompt = PromptTemplate(
            template=template,
            input_variables=["agent1","prompt1", "agent2", "prompt2"],
            partial_variables={"format_instructions": format_instructions}
            )

        _input = prompt.format_prompt(agent1=agent1, prompt1=prompt1, agent2=agent2, prompt2=prompt2)

        rules= output_parser.parse(self.llm(_input.to_string()))

        return rules

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
        self.rules = self.parse(self.llm(
            [HumanMessage(content=systemPrompt.content)]
        )) # syntax à revoir
    
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
        answer = self.parse(self.llm(
            [HumanMessage(content=systemPrompt.content)]
        ))
        print("answer: ", str(answer))
        return answer.split("\n")[-1] == "TRUE"
    
    def parse(self, message):   
        return message.content
    
    ## A compléter il faut une while loop and verif de la condition de terminaison
    def run(self, input):
        result = False
        while not result:
            print("agent2")
            output = self.agent2.getPrompt(input)
            result = self.check(output)
        
        result = False
        while not result:
            print("agent1")
            output = self.agent1.getPrompt(output)
            result = self.check(output)
            
        return output
    
    class Rules(BaseModel):
        agent: str = Field(description = "The agent that must comply with the constrain or the rule")
        rule: str = Field(description = "The rule or constrain short description")


            
                
    

  