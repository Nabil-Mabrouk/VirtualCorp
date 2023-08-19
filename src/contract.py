from langchain.chat_models import ChatOpenAI

class Contract():
    def __init__(self, agent1, agent2, llm=ChatOpenAI(temperature=0)):
        self.agent1=agent1
        self.agent2=agent2
        self.rules=[]
        self.initialize()
    
    def initialize(self):
        prompt1 = self.agent.getPrompt()
        prompt2 = self.agent.getPrompt()
        systemPrompt=""" Agent 1has recieved this prompt: {prompt1} and agent 2 has recieved the folowing prompt {prompt2}. 
                        Extract all the rules each agent has to fullfill during their interaction"""
        self.rules = parse(llm(systemPrompt)) # syntax à revoir
    
    def check(self, message):
        answer = 1
        systemPrompt=""" Check that this message: {message} respect all these rules : {self.rules}. You must answer TRUE if all the rules 
        are respect or FALSE if at least one rule is not respected"""
        answer= parse(llm(systemPrompt)) # à mettre dans un block try/except intelligent?    #syntax à revoir    
        return answer
    
    ## A compléter il faut une while loop and verif de la condition de terminaison
    def run(self, input):
        output = agent1.run(input)
        if self.check(output):
            agent2.run(output)
    

