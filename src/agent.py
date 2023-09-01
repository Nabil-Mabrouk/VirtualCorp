
from message import Message
from logger_config import logger
import streamlit as st

class Agent:
    """
    Represents an agent for interacting with a chatbot model.

    An agent can send and receive messages to/from a chatbot model.

    Args:
        name (str): The name of the agent.
        model (Model): The chatbot model to interact with.
        template (str): The template for formatting messages.
        ui (object, optional): User interface for agent interaction (e.g., Streamlit UI). Default is None.

    Attributes:
        name (str): The name of the agent.
        model (Model): The chatbot model associated with the agent.
        message (Message): A message formatter for creating formatted prompts.
        last_message (str): The last message sent or received by the agent.
        ui (object, optional): User interface for agent interaction (e.g., Streamlit UI). Default is None.

    Methods:
        run(input_dict): Send an input message to the chatbot model and receive a response.

    Example:
        >>> agent = Agent(name="User", model=my_model, template="Hello, <AGENT_NAME>. How can I assist you?")
        >>> user_input = {"AGENT_NAME": "ChatBot"}
        >>> response = agent.run(user_input)
        >>> print(response)

    """

    def __init__(self, name, model, template, ui=False):
        """
        Initializes a new Agent instance.

        Args:
            name (str): The name of the agent.
            model (Model): The chatbot model to interact with.
            template (str): The template for formatting messages.
            ui (object, optional): User interface for agent interaction (e.g., Streamlit UI). Default is None.
        """
        self.name = name
        self.model = model
        self.message = Message(template)
        self.last_message = ""
        self.ui = ui
    
    def run(self, input_dict):
        """
        Send an input message to the chatbot model and receive a response.

        Args:
            input_dict (dict): A dictionary containing placeholder-value pairs for message formatting.

        Returns:
            str: The response received from the chatbot model. None if an error occurs.
        """

        try:
            # Format the message prompt using the provided input dictionary
            logger.debug(f"[Agent: {self.name}] Running agent with input:\n {input_dict}")
            #if self.ui: st.success(f"Agent {self.name} constructing the prompt using input_dict: {input_dict} and the following prompt template : {self.message.template}")
            prompt = self.message.prompt(input_dict)
            #if self.ui: st.success(f"Agent {self.name} will run with the following prompt: {prompt}")
            # Send the formatted prompt to the chatbot model
            logger.debug(f"[Agent: {self.name}] Formatted prompt:\n {prompt}")
            #if self.ui: st.success(f"Running agent {self.name} with prompt: {prompt}")
            
            output = self.model.run(prompt)
            
            if self.ui: st.success(f"Agent {self.name} output: {output}")
            if output:
                self.last_message=output
                logger.info(f"{self.name}: {output}")
                return output
            else:
                logger.warning(f"[Agent {self.name} : ]No response received from the model.")
                #if self.ui:st.sucess(f"[Agent {self.name} : ]No response received from the model.")
                return None
        except Exception as e:
            logger.error(f"Error in agent {self.name}: {str(e)}")
            return None


        
        
