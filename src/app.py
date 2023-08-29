
import os
import openai
from dotenv import load_dotenv
import streamlit as st

# Access the secret key
load_dotenv()


from agent import Agent
from contract import Contract
from pipeline import Pipeline
from logger_config import logger
from model import HumanModel, GPTModel
import prompts as pts


def start():

    logger.info("WELCOM TO VirtualCORP - version 1.0 - 08/2023\n")

    # Define configuration
    model_name = "text-davinci-003"
    temperature = 0.1


    # Create model instances
    human_model = HumanModel()
    gpt_model1 = GPTModel(model_name, temperature)
    gpt_model2 = GPTModel(model_name, temperature)

    # Create the agents
    agent1=Agent(name="Client", model=human_model, template=pts.human_prompt)
    agent2=Agent(name="Welcome agent", model=gpt_model1, template=pts.agent_prompt)

    # Create the contract
    contract1=Contract("Business Validation", agent1=agent1, agent2=agent2, model=gpt_model2)

    pipeline = Pipeline(name="VirtualCorp", contracts=[contract1])
    pipeline.run(pts.human_prompt)

class Demo():
    def __init__(self):
        self.model = None
        self.user_interface = None

    def initiate_ui(self):
        st.title("VirtualCORP")
        presentation="""This project enables automated business creation with a focuss on compliance. 
        It involves agents, smart contracts, and pipelines to facilitate collaborative tasks."""
        st.info(presentation)
        self.tab1, self.tab2, self.tab3=st.tabs(["Home", "Doc", "Contact"])
        with self.tab1:
            st.header("Enter you business idea ..")
            st.info("Examples:\n - I would like to create an automated business to help clients measure their carbon footprint")
            selected_model_name = st.selectbox("Select Model:", list(models.keys()))
            self.model = models[selected_model_name]



if __name__ == '__main__':
    start()
    