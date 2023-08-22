class Message:
    def __init__(self, template):
        self.template = template

    def prompt(self, input_dict):
        """
        Replace placeholders in the template with corresponding values from a dictionary.

        Args:
            input_dict (dict): A dictionary with placeholder-value pairs.

        Returns:
            str: The template with placeholders replaced by their values.
        """
        message = self.template
        for key, value in input_dict.items():
            placeholder = f"<{key.upper()}>"
            message = message.replace(placeholder, value)
        return message
