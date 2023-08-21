import enum
from re import DEBUG
from langchain.llms.human import HumanInputLLM
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain.schema import HumanMessage, AIMessage


class AgentType(enum.Enum):
    HUMAN = 1
    VIRTUAL = 2
    
    
class Agent():
    def __init__(self, name, type=AgentType.HUMAN):
        self.name = name
        self.type = type
        self.template = ""
        self.prompt = ""
        self.input = ""
        self.output = ""
        self.llm = (ChatOpenAI(temperature=0) if type == AgentType.VIRTUAL
                   else HumanInputLLM(
                       prompt_func=lambda x: print(f"Agent {self.name} received prompt: {x}"),
                   ))
        
    def setTemplate(self, template):
        self.template = (HumanMessagePromptTemplate.from_template(template)
                         if self.type == AgentType.HUMAN
                         else AIMessagePromptTemplate.from_template(template))
        
    def step(self, inp, status, reasons):
        print(f"=======\n\nAgent {self.name}\nInput: {inp}\n")
        if self.type == AgentType.HUMAN:
            self.prompt = self.template.format(input=inp, status=status, reasons=reasons)
            self.output = self.llm(self.prompt.content)
            print(f"=======\n\nAgent {self.name}\nOutput: {self.output}\n")
            return self.output
        
        self.prompt = self.template.format(input=inp, status=status, reasons=reasons)
        self.output = self.llm(
            [AIMessage(content=self.prompt.content)]
        ).content
        print(f"=======\n\nAgent {self.name}\nOutput: {self.output}\n")
        return self.output
        
        
