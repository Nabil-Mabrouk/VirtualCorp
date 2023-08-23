from abc import ABC, abstractmethod
from logger_config import logger
from langchain.chat_models import ChatOpenAI
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Model(ABC):
    def __init__(self, model_name=None, temperature=None):
        self.model_name = model_name
        self.temperature=temperature

    @abstractmethod
    def run(self, input_text):
        pass

class HumanModel(Model):
    def run(self, prompt):
        user_input = input(prompt)
        return user_input

class GPTModel(Model):
    def __init__(self, model_name, temperature):
        super().__init__(model_name, temperature)

    def run(self, prompt):
        try:
            response = openai.Completion.create(
                engine=self.model_name,
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=2000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0)
            return response.choices[0].text.strip()
        except Exception as e:
            logger.error(f"Error in GPTModel.run(): {str(e)}\n Prompt = {prompt}")