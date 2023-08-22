from agent import Agent
from logger_config import logger


class Contract:
    def __init__(self, name, model, agent1, agent2, max_iter=10):
        self.name=name
        self.model=model
        self.agent1 = agent1
        self.agent2 = agent2

        # Extract Compliance rules
        self.agent1_rules = self.extract_rules(agent1, agent1.template, agent2.template)
        self.agent2_rules = self.extract_rules(agent2, agent2.template, agent1.template)
        
        # Extract termination keywords from the agent's prompt templates
        self.agent1_termination_keyword = self.extract_termination_keyword(agent1.prompt_template)
        self.agent2_termination_keyword = self.extract_termination_keyword(agent2.prompt_template)

        # Max number of interactions between agent1 and agent2
        self.max_interactions=max_iter
        self.iteraction_count=0
    
    def extract_rules(self, agent, agent_prompt, other_agent_prompt):
        # Create a prompt to extract rules for the given agent
        prompt = f"You are {agent}. Your prompt template is:\n\n{agent_prompt}\n\nFor this interaction, you will communicate with another agent using their prompt template:\n\n{other_agent_prompt}\n\nPlease provide the rules that {agent} must comply with."

        # Use the contract's language model to extract rules
        response = self.model.run(prompt)

        # Extract and return the rules from the model's response
        rules = response.choices[0].text.strip()
        return rules

    def extract_termination_keyword(self, agent_prompt):
        # Extract a termination keyword from the agent's prompt template
        # In the agent template the termination keyword must be enclosed in double curly braces, e.g., {{terminate}}
        keyword_start = agent_prompt.find("{{")
        keyword_end = agent_prompt.find("}}")

        if keyword_start != -1 and keyword_end != -1:
            return agent_prompt[keyword_start + 2:keyword_end]
        else:
            return None
        
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
                termination_keyword = self.agent1_termination_keyword
            else:
                sender:Agent = self.agent2
                receiver:Agent = self.agent1
                termination_keyword = self.agent2_termination_keyword

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