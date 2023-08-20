import enum
from re import DEBUG
from langchain import PromptTemplate
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
        self.llm = ChatOpenAI(temperature=0)
        
    def setTemplate(self, template):
        self.template = (HumanMessagePromptTemplate.from_template(template)
                         if self.type == AgentType.HUMAN
                         else AIMessagePromptTemplate.from_template(template))
        
    def step(self, inp):
        if self.type == AgentType.HUMAN:
            if DEBUG:        
                self.prompt = self.template.format(input=inp)
                self.output = self.llm(
                    [HumanMessage(content=self.prompt.content)]
                ).content
            else:
                self.output = input(inp)
                return self.output
        self.prompt = self.template.format(input=inp)
        self.output = self.llm(
            [AIMessage(content=self.prompt.content)]
        ).content
        
        return self.output
        
        
