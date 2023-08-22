from abc import ABC, abstractmethod
import openai
import os
from logger_config import logger
openai.api_key = os.getenv("OPENAI_API_KEY")

class Model(ABC):
    def __init__(self, model_name=None):
        self.model_name = model_name

    @abstractmethod
    def run(self, input_text):
        pass


class HumanModel(Model):
    def __init__(self):
        super().__init__()

    def run(self, input_text):
        # For human models, interactively collect input from the human
        user_input = input(f"[Human Model] Please provide your response to: {input_text}\nYour response: ")
        return user_input
    
class GPTModel(Model):
    def __init__(self, model_name):
        super().__init__(model_name)
        self.model = openai.Completion.create(
            engine=model_name,
            temperature=0.7,
            max_tokens=50
        )

    def run(self, input_text):
        # For language models, run the model and log the action
        response = self.model.run(input_text)
        logger.debug(f"[GPT Model] Running model with input: {input_text}")
        logger.debug(f"[GPT Model] Model raw response: {response}")
        output = response.choices[0].text.strip()
        logger.debug(f"[GPT Model] Model run method output: {output}")
        return output