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
        print(f"=======\n\nAgent {self.name}\nInput: {inp}\n")
        if self.type == AgentType.HUMAN:
            if DEBUG:        
                self.prompt = self.template.format(input=inp)
                self.output = self.llm(
                    [HumanMessage(content=self.prompt.content)]
                ).content
            else:
                self.output = input(inp)
            print(f"=======\n\nAgent {self.name}\nOutput: {self.output}\n")
            return self.output
        
        print(f"=======\n\nAgent {self.name}\nInput: {inp}\n")
        self.prompt = self.template.format(input=inp)
        self.output = self.llm(
            [AIMessage(content=self.prompt.content)]
        ).content
        
        print(f"=======\n\nAgent {self.name}\nOutput: {self.output}\n")
        return self.output
        
        
