from tabnanny import check

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.schema import HumanMessage

# from pydantic import BaseModel
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

from agent import Agent

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

            Format your answer as a list a list of confitions
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

        print(f"Extract :({to_extract}): {output}")

        return output






    def _extract_rules(self):
        agent1 = self.agent1.name
        prompt1 = self.agent1.template

        agent2 = self.agent2.name
        prompt2 = self.agent2.template

        response_schemas = [
            ResponseSchema(name="agent", description="Name of the agent"),
            ResponseSchema(
                name="compliance_rule", description="Rule or constrain that the agent must comply with"),
            ResponseSchema(
                name="termination_rule", description="Rule to terminate the interaction with the agent"),
        ]
        
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        
        format_instructions = output_parser.get_format_instructions()

        template = """
            The agent named {agent1} recieved the following prompt:
            Prompt: {prompt1}

            The agent named {agent2} recieved the following prompt
            Prompt: {prompt2}

            From these prompts extract, the rules and constrain that each agent should comply with
            {format_instructions}
            All formatted in a JSON list.
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["agent1", "prompt1", "agent2", "prompt2"],
            partial_variables={"format_instructions": format_instructions}
        )

        _input = prompt.format_prompt(
            agent1=agent1, prompt1=prompt1, agent2=agent2, prompt2=prompt2)

        _output = self.llm([HumanMessage(content=_input.to_string())]).content
        rules = output_parser.parse(_output)

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
        ))


    def _check(self, message, sender):
        answer = 1
        checkPrompt = """
        You will be provided with a message sent by a sender and a list of compliance rule and termination rules.
        You must check if the message is compliant with the compliance rules and if the termination condition is satisfied.
        You must answer only by "COMPLIANT", "COMPLIANT AND TERMINATED", "NON COMPLIANT"
        -----
        message: {message}
        -----
        sender: {sender}
        -----
        compliance rules: {rules}
        -----
        termination rules: {termination}

        ----
        You output must be one of these choices and nothing else: "COMPLIANT", "COMPLIANT AND TERMINATED", "NON COMPLIANT"
        """
        systemPrompt = (SystemMessagePromptTemplate
                        .from_template(checkPrompt)
                        .format(message=message, sender=sender,rules=self.rules, termination=self.termination))
        # à mettre dans un block try/except intelligent?    #syntax à revoir
        answer = self.parse(self.llm(
            [HumanMessage(content=systemPrompt.content)]
        ))
        print(f"Contract: {self.name} - Message from agent: {sender} - Status = ", str(answer))
        return answer.split("\n")[-1]
    
    def check(self, message):
        answer = 1
        checkPrompt = """
        Check that this message: {message} respect all these rules : {rules}. You must answer:
        - TERMINATED if all the compliance rules are respected and the termination rules are respected.
        - COMPLIANT if only all the compliance rules are respected.
        - NON-COMPLIANT if at least one compliance rule is not respected.
        """
        systemPrompt = (SystemMessagePromptTemplate
                        .from_template(checkPrompt)
                        .format(message=message, rules=self.rules))
        # à mettre dans un block try/except intelligent?    #syntax à revoir
        answer = self.parse(self.llm(
            [HumanMessage(content=systemPrompt.content)]
        ))
        print("Method chek: answer: ", str(answer))
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
        
        while not termination and not compliance and iteration < 10:
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
