
from message import Message
from logger_config import logger

class Agent:
    def __init__(self, name, model, template):
        self.name=name
        self.model=model
        self.message = Message(template)
    
    def run(self, input_dict):
        logger.info(f"[{self.name}] Running agent with input: {input_dict}")
        prompt = self.message.replace_placeholders(input_dict)

        logger.debug(f"[{self.name}] Formatted prompt: {prompt}")
        output = self.model.run(prompt)

        logger.debug(f"[{self.name}] Agent output: {output}")
        return output

        
        
