from logger_config import logger
import prompts as pts
from message import Message
import json
import streamlit as st
 
class Contract:
    """
    Represents a contract between two agents, which is executed as a conversation.
    
    Attributes:
        name (str): The name of the contract.
        model (object): The language model used to evaluate compliance.
        prompt_template (str): The template for generating prompts during the contract.
        agent1 (Agent): The first agent participating in the contract.
        agent2 (Agent): The second agent participating in the contract.
        max_iter (int, optional): The maximum number of interactions between agent1 and agent2 (default is 10).
        max_iter_compliance (int, optional): The maximum number of interactions between an agent and the contract to enforce compliance (default is 3).
        ui (object, optional): The user interface object for interaction (default is None).
        termination_keyword (str): A keyword that agents use to signal the contract's termination.

    Methods:
        check(sender, message, rules=None):
            Checks compliance of a message sent by an agent.
        
        run(input):
            Runs the contract as a conversation between agent1 and agent2.
    """



    def __init__(self, name, model, prompt_template, agent1, agent2, max_iter=10, max_iter_compliance=3, ui=False):
        """
        Initializes a new Contract instance.

        Args:
            name (str): The name of the contract.
            model (object): The language model used to evaluate compliance.
            prompt_template (str): The template for generating prompts during the contract.
            agent1 (Agent): The first agent participating in the contract.
            agent2 (Agent): The second agent participating in the contract.
            max_iter (int, optional): The maximum number of interactions between agent1 and agent2 (default is 10).
            max_iter_compliance (int, optional): The maximum number of interactions between an agent and the contract to enforce compliance (default is 3).
            ui (object, optional): The user interface object for interaction (default is False).
        """
        self.name = name
        self.model = model
        self.prompt_template = prompt_template
        self.agent1 = agent1
        self.agent2 = agent2
        self.ui = ui
        self.termination_keyword = "terminated"
        self.max_interactions = max_iter
        self.interaction_count = 0
        self.max_iter_compliance = max_iter_compliance
        self.delivery=dict(name="")

        
    def check(self, sender, message, rules=None):
        """
        Checks compliance of a message sent by an agent.

        Args:
            sender (Agent): The agent sending the message.
            message (str): The message content to be checked for compliance.
            rules (str, optional): The compliance rules (default is None, deduced from sender's agent prompt).

        Returns:
            dict: A dictionary indicating compliance status.
        """
        #if self.ui: st.info(f"Starting compliance text for message sent by : {sender.name}")
        #if self.ui: st.info(f" Compliance test for message: {message}")
        if rules:
            input_dict={'QUERY':message, "RULES":rules}
        else:
            input_dict={'QUERY':message, "RULES":str(sender.message.template)}
        #if self.ui: st.info(f" Creating prompt for compliance test- input_dict = : {input_dict} using prompt template: {self.prompt_template}")
        # Generate the prompt of the contract
        prompt=Message(self.prompt_template).prompt(input_dict)
        #if self.ui: st.info(f" Prompt for compliance test: {prompt}")
        logger.info(f"[Contract: {self.name} - check]: checking compliance of message of agent : {sender.name}\n Prompt = {prompt}")

        try:
            output = self.model.run(prompt)
            #if self.ui: st.info(f" Result of the compliance test: {output}")
            output=self.parser(output)
            logger.debug(f"[Contract: {self.name}] - Compliance test raw output: {output}")
            
            try:
                logger.debug(f"[Contract: {self.name}] - Verifying the model output: {output}")
                compliance_result = json.loads(output)
                
                # Check if the compliance_result has expected keys
                if "Answer" in compliance_result and "Reasoning" in compliance_result:
                    return compliance_result
                else:
                    logger.error(f"[Contract: {self.name} - check compliance] - Unable to find the keys in the model output")
                    raise ValueError("Invalid compliance_result format")
            except json.JSONDecodeError:
                logger.error(f"[Contract: {self.name} - check compliance] - The model returns a bad formatted output. Check your prompt. \
                             Le contract must return a json with two keys: <Answer> and <Reasoning>")

                raise ValueError("Invalid JSON format in compliance_result")
            
        except Exception as e:
            logger.error(f"[Contract: {self.name}] Error while running the compliance check model", str(e))
            # Return a dictionary indicating failure
            return {'compliance': 'failure', 'reasoning': str(e)}

    
    def run(self, input):
        """
        Runs the contract as a conversation between agent1 and agent2.

        Args:
            input (str): The initial input for the contract.

        Returns:
            str: The final output of the contract.
        """
        feedback=""
        while self.interaction_count < self.max_interactions:
            sender = self.get_sender_and_receiver()
            self.log_interaction_start()
            compliance_check=0
            output = self.run_sender(sender, input, feedback)["Answer"]
            compliance = self.check(sender, output)
            compliance_check +=1

            if self.ui: st.info(f" Compliance Results: {compliance}")
            if compliance['Answer'] in ["Compliant", "Neutral"]:
                input=output
                self.interaction_count +=1
                feedback=""
            else:
                feedback = compliance['Reasoning']
                self.handle_non_compliance(sender)

            if self.is_termination_condition_met(output):
                self.log_termination_condition_met()
                break

        return output

    def get_sender_and_receiver(self):
        """
        Determines the sender and receiver agents based on the interaction count.

        Returns:
            Tuple[Agent, Agent]: The sender and receiver agents.
        """
        if self.interaction_count % 2 == 0:
            sender = self.agent1
        else:
            sender = self.agent2
        return sender

    def log_interaction_start(self):
        """
        Logs the beginning of a new interaction.
        """
        logger.debug(f"[Contract: {self.name}] Starting interaction. Iteration: {self.interaction_count}")
        if self.ui: st.info(f"Contract {self.name} - Interaction N° {self.interaction_count}..")

    def run_sender(self, sender, input, feedback):
        """
        Runs the sender's agent with the given input.

        Args:
            sender (Agent): The sender agent.
            input (str): The input for the sender.

        Returns:
            str: The output of the sender.
        """
        logger.debug(f"[Contract {self.name}:] Running sender ({sender.name}) with input \n {input}")
        try:
            #if self.ui: st.info(f"Running sender (name={sender.name}) with the following input :\n {input}")
            output = sender.run({"MESSAGE": input, 'FEEDBACK':feedback, 'LAST_MESSAGE': sender.last_message}) 
            if(output): 
                #if self.ui: st.warning(f" before parser: {output}")
                output=self.parser(output)
                #if self.ui: st.warning(f" after parser: {output}")
                try:
                    output= json.loads(output)
                except Exception as e:
                    if self.ui: st.error(" can't convert to json")
          
            
                #if self.ui: st.warning(output)
                 #if self.ui: st.info(f"Sender {sender.name} generated message:\n {output}")
                logger.debug(f"[Contract: {self.name}] Sender's output: {output}")
        except Exception as e:
            logger.error(f"[Contract: {self.name}]: Error while calling the model of agent: {sender.name}: {str(e)}")
        sender.last_message=output['Answer']
        return output

    def check_compliance(self, sender, output):
        """
        Checks compliance of the output message from the sender.

        Args:
            sender (Agent): The sender agent.
            output (str): The output message from the sender.

        Returns:
            dict: A dictionary with 'compliance' and 'reasoning' keys.
        """
        #if self.ui: st.info(f"Checking_compliance of input: {output}")
        input_dict = {'QUERY': str(output), "RULES": str(sender.message.template)}
        prompt = Message(self.prompt_template).prompt(input_dict)
        logger.info(f"[Contract: {self.name} - check]: checking compliance of message of agent : {sender.name}\n Prompt = {prompt}")

        try:
            compliance_result = json.loads(self.model.run(prompt))
            if "Answer" in compliance_result and "Reasoning" in compliance_result:
                return {'compliance': compliance_result['Answer'], 'reasoning': compliance_result['Reasoning']}
            else:
                raise ValueError("Invalid compliance_result format")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in compliance_result")
        except Exception as e:
            logger.error(f"[Contract: {self.name}] Error while checking compliance: {str(e)}")
            return {'compliance': 'failure', 'reasoning': str(e)}

    def handle_non_compliance(self, sender):
        """
        Handles non-compliant messages from the sender.

        Args:
            sender (Agent): The sender agent.
        """
        input = sender.message.template
        logger.warning(f"[Contract: {self.name}] Sender ({sender.name}) provided a non-compliant or neutral message. Retrying.")

    def is_termination_condition_met(self, output):
        """
        Checks if the termination condition is met based on the output message.

        Args:
            output (str): The output message.

        Returns:
            bool: True if the termination condition is met, False otherwise.
        """
        if self.termination_keyword and self.termination_keyword in output:
            logger.info("f[Contract: {self.name}] Termination condition met. Ending interaction.")
            return True
        return False

    def log_termination_condition_met(self):
        """
        Logs the termination condition being met.
        """
        logger.info("f[Contract: {self.name}] Termination condition met. Ending interaction.")
    
    def parser(self, input_string):
        try:
            # Find the JSON part of the string (assuming it starts with 'Answer:')
            start_index = input_string.find('{')
            end_index = input_string.rfind('}')
            if start_index != -1 and end_index != -1:
                json_string = input_string[start_index:end_index + 1]
                # Parse the JSON data
                #json_data = json.loads(json_string)
                return json_string
            else:
                if self.ui: st.error(f"unable to parse string :{input_string}")
                raise ValueError("JSON data not found in the input string.")
        except Exception as e:
            logger.error(f"Error parsing JSON: {str(e)}")
            return None


