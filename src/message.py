from logger_config import logger
import streamlit as st
import json
class Message:
    def __init__(self, template, placeholder_start="<", placeholder_end=">"):
        """
        Initialize a message with a template and optional custom placeholder markers.

        Args:
            template (str): The message template with placeholders.
            placeholder_start (str, optional): The start marker for placeholders. Default is "<".
            placeholder_end (str, optional): The end marker for placeholders. Default is ">".
        """
        self.template = template
        self.placeholder_start = placeholder_start
        self.placeholder_end = placeholder_end

    def prompt(self, input_dict):
        """
        Replace placeholders in the template with corresponding values from a dictionary.

        This method takes a dictionary containing placeholder-value pairs and substitutes
        the placeholders in the message template with their corresponding values.

        Args:
            input_dict (dict): A dictionary with placeholder-value pairs.

        Returns:
            str: The template with placeholders replaced by their values. If a placeholder
            is not found in the input_dict, it will remain unchanged in the output.

        Example:
        ```python
        message_template = "Hello, <NAME>! Your account balance is $<BALANCE>."
        input_dict = {"NAME": "John", "BALANCE": "1000"}
        message = Message(message_template)
        result = message.prompt(input_dict)
        # Output: "Hello, John! Your account balance is $1000."
        ```
        """
        message = self.template
        for key, value in input_dict.items():
            placeholder = f"{self.placeholder_start}{key}{self.placeholder_end}"
            #st.write(f"[Message]: placeholder: {placeholder}, value: {value}")
            message = message.replace(placeholder, value)
        
        #st.write(f"[Message]: message: {message}")
        return message
    



