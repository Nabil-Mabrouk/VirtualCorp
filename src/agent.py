
from message import Message
from logger_config import logger


class Agent:
    def __init__(self, name, model, template):
        self.name=name
        self.model=model
        self.message:Message=Message(template)
        self.last_message=""
    
    def run(self, input_dict):
        logger.info(f"[Agent: {self.name}] Running agent with input:\n {input_dict}")
        prompt = self.message.prompt(input_dict)

        logger.debug(f"[Agent: {self.name}] Formatted prompt:\n {prompt}")
        output = self.model.run(prompt)
        self.last_message=output

        logger.debug(f"[Agent: {self.name}] Agent output: {output}")
        return output

        
        
