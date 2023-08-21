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
        self.MAX_ITER = int(os.getenv("MAX_ITER"))

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

            - the rules and constrain that {agent1} must comply with and do not terminate the interaction
            - the rules and constrains that {agent2} must comply with and do not terminate the interaction

            format your answer as a list two columns: ['agent', 'rule']
        """
        template2 = """
            The agent named {agent1} recieved the following prompt:
            Prompt: {prompt1}

            The agent named {agent2} recieved the following prompt
            Prompt: {prompt2}

            From these prompts extract:

            - the exact conditions that, if fulfilled, the interaction between the two agents must be terminated

            format your answer as a list two columns: ['agent', 'rule']
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
        You will be provided with a message sent by a sender and a list of compliance rule and termination rules.
        You must check if the message is compliant with the compliance rules and if the termination condition is satisfied.
        -----
        message: {message}
        -----
        sender: {sender}
        -----
        compliance rules: {rules}
        -----
        termination rules: {termination}

        ----
        
        Your final decision should formatted as follow:
        
        
        REASON: <YOUR_REASON>
        Decision: <YOUR_DECISION>
        
        <YOUR_DECISION> may be one of the following:
        - COMPLIANT If compliant and not terminated
        - NON_COMPLIANT If not compliant
        - COMPLIANT_AND_TERMINATED If compliant and terminated
        """
        # In the case where you answer is "NON COMPLIANT" and only in this case 
        systemPrompt = (SystemMessagePromptTemplate
                        .from_template(checkPrompt)
                        .format(message=message, sender=sender.name,rules=self.rules, termination=self.termination))
        # à mettre dans un block try/except intelligent?    #syntax à revoir
        answer = self.parse(self.llm(
            [HumanMessage(content=systemPrompt.content)]
        ))
        print(f"=======\nContract: {self.name}\nMessage from agent: {sender.name}\nStatus =\n", str(answer))
        print(f"\n")
        return answer, answer.split("Decision: ")[-1]
    

    def parse(self, message):
        return message.content
    

    def run(self, input):
        terminated = False
        iteration = 0

        # if NOT COMPLIED --> exit while loop ?
        # attention si Terminated on doit retourner les deux derniers outputs sinon on peut ne retourner 
        # que la formule de terminaison (dernier output exemple I agree)ce qui ne sert à rien au contrat suivant
       
        output_agent2 = input 
        while not terminated and iteration < self.MAX_ITER:
            input_agent1 = output_agent2
            terminated, output_agent1 = self.check_agent(self.agent1, input_agent1)
            if not terminated:
                input_agent2 = output_agent1
                terminated, output_agent2 = self.check_agent(self.agent2, input_agent2)
            iteration += 1

        return output_agent1, output_agent2

    def check_agent(self, agent, input):
        iteration = 0
        compliant = False
        terminated = False
        status = "COMPLIANT"
        reasons = "Waiting for your message"
        while not compliant and iteration < self.MAX_ITER:
            print(f"=======\nContract: {self.name} - Iteration: {iteration}\n")
            output = agent.step(input, status, reasons)
            reasons, status = self._check(output, sender=agent)
            compliant =  status in ["COMPLIANT", "COMPLIANT_AND_TERMINATED"]
            terminated = status in ["COMPLIANT_AND_TERMINATED"]
            iteration += 1
        return terminated, output