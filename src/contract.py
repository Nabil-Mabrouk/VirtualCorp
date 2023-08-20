from tabnanny import check

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.schema import HumanMessage

# from pydantic import BaseModel
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

from agent import Agent
from dotenv import load_dotenv
# Access the secret key
load_dotenv()
import os

# ajouter un nom au contrat pour mieux l'identifier dans le log ou dans les print. Branch new --> [DONE]


class Contract():
    def __init__(self, name, agent1, agent2, llm=ChatOpenAI(temperature=0)):
        self.name = name
        self.agent1: Agent = agent1
        self.agent2: Agent = agent2
        self.llm = llm
        #self.rules = self._extract_rules()
        self.termination = self._extract("termination")
        self.rules = self._extract("rules")
        self.MAX_ITER=os.getenv("MAX_ITER")

    def _extract(self, to_extract):
        agent1 = self.agent1.name
        prompt1 = self.agent1.template

        agent2 = self.agent2.name
        prompt2 = self.agent2.template

        template1 = """
            The agent named {agent1} recieved the following prompt:
            Prompt: {prompt1}

            The agent named {agent2} recieved the following prompt
            Prompt: {prompt2}

            From these prompts extract:

            - the rules and constrain that {agent1} must comply with
            - the rules and constrains that {agent2} must comply with

            format your answer as a list two columns: ['agent', 'rule']
        """
        template2 = """
            The agent named {agent1} recieved the following prompt:
            Prompt: {prompt1}

            The agent named {agent2} recieved the following prompt
            Prompt: {prompt2}

            From these prompts extract:

            - the conditions that must be fullfilled to end the interaction between the two agents

            Format your answer as a list of conditions
        """

        if to_extract=="rules":
            template=template1
        else:
            template=template2

        prompt = PromptTemplate(
            template=template,
            input_variables=["agent1", "prompt1", "agent2", "prompt2"],
        )

        _input = prompt.format_prompt(
            agent1=agent1, prompt1=prompt1, agent2=agent2, prompt2=prompt2)

        output = self.llm([HumanMessage(content=_input.to_string())]).content

        print(f"Extract :\n({to_extract}): {output}")

        return output


    def _check(self, message, sender):
        answer = 1
        checkPrompt = """
        You will be provided with a message sent by a sender and a list of compliance rules and termination conditions.
        You must check if the message is compliant with the compliance rules and if the termination condition are satisfied.
        You must answer only by "COMPLIANT", "COMPLIANT AND TERMINATED", "NON COMPLIANT"
        In the case where you answer is "NON COMPLIANT" and only in this case you must explain why it is non compliant.
        -----
        message: {message}
        -----
        sender: {sender}
        -----
        compliance rules: {rules}
        -----
        termination rules: {termination}

        ----
        Your output must be one of these choices and nothing else: "COMPLIANT", "COMPLIANT AND TERMINATED", "NON COMPLIANT"
        """
        systemPrompt = (SystemMessagePromptTemplate
                        .from_template(checkPrompt)
                        .format(message=message, sender=sender,rules=self.rules, termination=self.termination))
        # à mettre dans un block try/except intelligent?    #syntax à revoir
        answer = self.parse(self.llm(
            [HumanMessage(content=systemPrompt.content)]
        ))
        print(f"=======\nContract: {self.name} - Message from agent: {sender} - Status = ", str(answer))
        print(f"\n")
        return answer.split("\n")[-1]
    

    def parse(self, message):
        return message.content
    

    def run(self, input):
        compliance = False
        termination = False
        iteration = 0

        # if NOT COMPLIED --> exit while loop ?
        # attention si Terminated on doit retourner les deux derniers outputs sinon on peut ne retourner 
        # que la formule de terminaison (dernier output exemple I agree)ce qui ne sert à rien au contrat suivant
        
        while not termination and not compliance and iteration < self.MAX_ITER:
            print(f"=======\nContract: {self.name} - Iteration: {iteration}\n")
            output = self.agent1.step(input)
            status = self._check(output, sender=self.agent1.name)
            compliance =  status in ["COMPLIANT", "COMPLIANT AND TERMINATED"]
            termination = status in ["COMPLIANT AND TERMINATED"]

            input = self.agent2.step(output)
            status = self._check(input, sender=self.agent2.name)
            compliance =  status in ["COMPLIANT", "COMPLIANT AND TERMINATED"]
            termination = status in ["COMPLIANT AND TERMINATED"]
            iteration += 1

        return output
    
    def run(self, input):
        compliance = False
        termination = False
        iteration = 0

        # if NOT COMPLIED --> exit while loop ?
        # attention si Terminated on doit retourner les deux derniers outputs sinon on peut ne retourner 
        # que la formule de terminaison (dernier output exemple I agree)ce qui ne sert à rien au contrat suivant
        
        while not termination and not compliance and iteration < 10:
            print(f"=======\nContract: {self.name} - Iteration: {iteration}\n")
            output = self.agent1.step(input)
            status = self._check(output, sender=self.agent1.name)
            compliance =  status in ["COMPLIANT", "COMPLIANT AND TERMINATED"]
            termination = status in ["COMPLIANT AND TERMINATED"]

            input = self.agent2.step(output)
            status = self._check(input, sender=self.agent2.name)
            compliance =  status in ["COMPLIANT", "COMPLIANT AND TERMINATED"]
            termination = status in ["COMPLIANT AND TERMINATED"]
            iteration += 1

        return output
