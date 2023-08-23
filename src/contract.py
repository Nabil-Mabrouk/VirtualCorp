from agent import Agent
from logger_config import logger
import prompts as pts
from message import Message

class Contract:
    def __init__(self, name, model, agent1, agent2, max_iter=10):
        self.name=name
        self.model=model
        self.agent1:Agent = agent1
        self.agent2:Agent = agent2

        # Extract Compliance rules
        input_dict1={"First agent name":self.agent1.name,
                    "Second agent name":self.agent2.name,
                    "First agent instructions": self.agent1.message.template,
                    "Second agent instructions": self.agent2.message.template,
                    "extract rules for agent":self.agent1.name #extract rules for Agent 1
                    }
        input_dict2={"First agent name":self.agent1.name,
                    "Second agent name":self.agent2.name,
                    "First agent instructions": self.agent1.message.template,
                    "Second agent instructions": self.agent2.message.template,
                    "extract rules for agent":self.agent2.name #extract rules for Agent 2
                    }
        
        prompt1=Message(pts.extract_rules_template).prompt(input_dict1)
        prompt2=Message(pts.extract_rules_template).prompt(input_dict2)

        self.agent1_rules = self.extract_rules(prompt1)
        self.agent2_rules = self.extract_rules(prompt2)
        
        prompt=Message(pts.extract_termination_keywords).prompt(input_dict1)

        # Extract termination keywords from the agent's prompt templates
        self.termination_keyword = self.extract_termination_keyword(prompt)

        # Max number of interactions between agent1 and agent2
        self.max_interactions=max_iter
        self.iteraction_count=0

        # logging
        logger.info(f"[Contract: {self.name}]: Between agent 1: {self.agent1.name} and agent 2: {self.agent2.name}")
        logger.info(f"[Contract: {self.name}]: Compliance rule for agent 1: {self.agent1.name}:\n {self.agent1_rules}")
        logger.info(f"[Contract: {self.name}]: Compliance rule for agent 2: {self.agent2.name}:\n {self.agent2_rules}")
        logger.info(f"[Contract: {self.name}]: Termination keywords:\n {self.termination_keyword}")
    
    def extract_rules(self, prompt):
        
        # Use the contract's language model to extract rules
        rules = self.model.run(prompt)

        # logging for debug
        logger.debug(f"[Contract: {self.name}]: Rule extraction prompt: {prompt}")
        logger.debug(f"[Contract: {self.name}]: Language model results: {rules}")

        return rules

    def extract_termination_keyword(self, prompt):
        
        # Use the contract's language model to extract rules
        rules = self.model.run(prompt)

        return rules
        
    def check(self, sender: Agent, message):
        if sender == self.agent1:
            # Check if the message of Agent 1 is compliant with Agent 1's rules
            prompt = f"Check if the message of Agent: {sender.name} is compliant with Agent {sender.name} rules.\n\nMessage: {message}\n\nRules: {self.agent1_rules} \n\n You answer should be: 'COMPLIANT' or 'NON COMPLIANT because ..' and explain why it is non compliant"
        elif sender == self.agent2:
            # Check if the message of Agent 2 is compliant with Agent 2's rules
            prompt = f"Check if the message of Agent: {sender.name} is compliant with Agent {sender.name}.\n\nMessage: {message}\n\nRules: {self.agent2_rules}\n\n You answer should be: 'COMPLIANT' or 'NON COMPLIANT because ..' and explain why it is non compliant"
        else:
            raise ValueError("Invalid sender")

        # Use the contract's language model to check compliance
        try:
            feedback = self.model(prompt)
            logger.debug(f"[Contract: {self.name}] - Compliance test feedback: {feedback}")
        except Exception as e:
            logger.error("[Contract: {self.name}] Error while checking compliance:", str(e))

        if feedback.lower() == "compliant":
            return "compliant"
        else:
            # Return a prompt to the sender for a second chance
            return f"Your last message is {feedback}. Please review your message and provide a compliant response."

    
    def run(self, input):
        while self.interaction_count < self.max_interactions:
            if self.interaction_count % 2 == 0:
                sender:Agent = self.agent1
                receiver:Agent = self.agent2
                termination_keyword = self.termination_keyword
            else:
                sender:Agent = self.agent2
                receiver:Agent = self.agent1
                termination_keyword = self.termination_keyword

            # Log the beginning of a new interaction
            logger.info(f"[Contract: {self.name}] Starting interaction {self.interaction_count + 1}")

            # Run the sender's agent
            logger.debug(f"[Contract: {self.name}] Running sender ({sender.name}) with input: {input}")
            try:
                output = sender.run(input)
                logger.debug(f"[Contract: {self.name}] Sender's output: {output}")
            except Exception as e:
                logger.error(f"[Contract: {self.name}]: Error while calling the model of agent: {sender.name}: ", str(e))
            

            # Check compliance and provide feedback
            compliance = self.check(sender, output)
            logger.debug(f"[Contract: {self.name}] Compliance check result: {compliance}")

            if compliance == "compliant":
                # Run the receiver's agent
                logger.debug(f"[Contract: {self.name}] Running receiver ({receiver.name}) with input: {output}")
                output = receiver.run(output)
                logger.debug(f"[Contract: {self.name}] Receiver's output: {output}")
                self.interaction_count += 1
            else:
                # If the message is not compliant, the sender gets a second chance
                # by providing a compliant response.
                input = compliance
                logger.warning(f"[Contract: {self.name}] Sender ({sender.name}) provided a non-compliant message. Retrying.")

            # Check if the termination keyword is present in the message
            if termination_keyword and termination_keyword in output:
                logger.info("f[Contract: {self.name}] Termination condition met. Ending interaction.")
                break

        return output