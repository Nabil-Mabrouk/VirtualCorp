from abc import ABC, abstractmethod
from logger_config import logger
from langchain.chat_models import ChatOpenAI
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
import streamlit as st

class Model(ABC):
    """
    Abstract base class for chatbot models.

    This class defines the basic structure and behavior expected from chatbot models.
    Subclasses must implement the abstract method `run` to define how the model processes input.

    Args:
        model_name (str): The name of the chatbot model.
        temperature (float, optional): The temperature parameter for generating responses.
        max_token (int, optional): The maximum number of tokens in the generated response.
        ui (object, optional): User interface for user interaction (e.g., Streamlit UI).

    Attributes:
        model_name (str): The name of the chatbot model.
        temperature (float, optional): The temperature parameter for generating responses.
        max_token (int, optional): The maximum number of tokens in the generated response.
        ui (object, optional): User interface for user interaction (e.g., Streamlit UI).

    """

    def __init__(self, model_name=None, temperature=None, max_token=None, ui=None):
        self.model_name = model_name
        self.max_token = max_token
        self.temperature = temperature
        self.ui = ui

    @abstractmethod
    def run(self, input_text):
        """
        Process input and generate a response.

        This method must be implemented by subclasses to define how the chatbot model processes
        input and generates a response.

        Args:
            input_text (str): The input text or prompt.

        Returns:
            str: The generated response.
        """
        pass

class HumanModel(Model):
    """
    Chatbot model representing a human user for user interaction.

    This model allows interaction with a chatbot through a user interface, such as Streamlit.
    It prompts the user for input and returns the user's responses.

    Args:
        ui (object, optional): User interface for user interaction (e.g., Streamlit UI). Default is None.

    """

    def __init__(self, ui=False):
        super().__init__(ui=ui)
        self.iter=0

    def run(self, prompt):
        """
        Prompt the user for input and return their response.

        Args:
            prompt (str): The prompt or message to display to the user.

        Returns:
            str: The user's response.
        """
        if self.ui:
            if prompt is not None:
                st.warning(prompt)

            # Use user interface for input if provided
            name=str(self.iter)

            form=st.form(name, clear_on_submit=True)
            with form:
                user_input = st.text_input("Type your answer here")  # Unique key
                is_terminated=st.checkbox("Terminated")

                submitted = st.form_submit_button("Submit")
                if submitted:
                    self.iter+=1
                    if is_terminated: output='{"Answer":"terminated"}'
                    else:
                        output='''{"Answer":"'''+user_input+'"}'
                    return str(output)
                else:
                    st.stop()

            #if next_button:
            #    self.ui.warning("Thank you - Contract terminated")
            #    user_input = "terminated"
            #    return user_input
        else:
            # Fall back to standard command-line input
            return input("Type your answer here: ")



class GPTModel(Model):
    """
    Chatbot model using the OpenAI GPT model for generating responses.

    This model interacts with the OpenAI GPT model to generate responses based on the provided prompt.

    Args:
        model_name (str): The name of the GPT model.
        temperature (float): The temperature parameter for response generation.
        max_token (int): The maximum number of tokens in the generated response.
        ui (object): User interface for user interaction (e.g., Streamlit UI).

    """

    def __init__(self, model_name, temperature, max_token, ui):
        super().__init__(model_name, temperature, max_token, ui)

    def run(self, prompt):
        """
        Generate a response based on the provided prompt.

        Args:
            prompt (str): The prompt or message to provide to the GPT model.

        Returns:
            str: The generated response.
        """
        try:
            response = openai.Completion.create(
                engine=self.model_name,
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_token,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            logger.error(f"Error in GPTModel.run(): {str(e)}\n Prompt = {prompt}")
