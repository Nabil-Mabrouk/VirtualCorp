import enum


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
        
    def setTemplate(self, template):
        self.template = template
        
    def getPrompt(self, *args):
        if self.type == AgentType.HUMAN:
            self.output = (input("Please enter your business idea : ")
                           or "Launch an ecommerce business to trade 3d printed parts")
            return self.output
        self.output = self.template.format_messages(input)
        return self.output
        
        
