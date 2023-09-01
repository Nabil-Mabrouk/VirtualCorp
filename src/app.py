import streamlit as st
from agent import Agent
from contract import Contract
from pipeline import Pipeline
from logger_config import logger
from model import HumanModel, GPTModel
import prompts as pts
import delivery as dlv



# LLM Models
models ={
    'text-davinci-003':{
        'name':'text-davinci-003',
        'temperature':1,
        'max_tokens':2000,
    }
}

class App:
    def __init__(self):
        self.model = None
        self.with_ui = True
        self.dlv=dlv.Deliveries()

    def initiate_ui(self):
        # Set up the Streamlit app title and introduction
        st.title("VirtualCORP")
        presentation = """This project enables automated business creation with a focus on compliance. 
        It involves agents, smart contracts, and pipelines to facilitate collaborative tasks."""
        st.info(presentation)

        # Insert an image below the information
        st.image('img/VirtualCorp.jpg', use_column_width=True) 

        #Insert a sidebar to select and config the model
        with st.sidebar:
            openai_api_key= st.text_input("OpenAI API key", value="", type="password")
            st.caption(
                "*If you don't have an OpenAI API key, get it [here](https://platform.openai.com/account/api-keys).*")
            selected_model = st.selectbox("Model", list(models.keys()))
            self.model=models[selected_model]
            self.model["temperature"]=st.slider("Temperature", 0.0, 2.0)
            self.model["max_tokens"]=st.slider("Max Token", 500, 2000)

        # Create tabs for different sections
        tab1, tab2, tab3 = st.tabs(["Home", "Documentation", "Contact"])

        with tab1:
            tab1.subheader("Enter your business idea ..")
            tab1.info("Examples:\n - I would like to create an automated business to help clients measure their carbon footprint")

        with tab2:
            tab2.header("Documentation")

        with tab3:
            tab3.header("Contact")

    def start(self):

        logger.info("WELCOM TO VirtualCORP - version 1.0 - 08/2023\n")

        if self.with_ui is False:

            # ask user to select model, temperature and max_token (provide choices from models)
            self.model=models['text-davinci-003']

        # Create model instances
        human_model = HumanModel(ui=self.with_ui)
        gpt_model1 = GPTModel(self.model['name'], self.model['temperature'], self.model['max_tokens'], ui=self.with_ui)
        gpt_model2 = GPTModel(self.model['name'], self.model['temperature'], self.model['max_tokens'], ui=self.with_ui)


        # Create the agents
        agent1 = Agent(name="Client", model=human_model, template=pts.human_prompt, ui=self.with_ui)
        agent2 = Agent(name="Welcome agent", model=gpt_model1, template=pts.agent_prompt, ui=self.with_ui)


        # Create the contract
        contract1 = Contract(name="Business Validation",
                             model=gpt_model2,
                             prompt_template=pts.contract_prompt,
                             agent1=agent1,
                             agent2=agent2,
                             ui=self.with_ui,
                             max_iter=10,
                             max_iter_compliance=3)

        # Create the pipeline
        pipeline = Pipeline(name="VirtualCorp", contracts=[contract1], ui=self.with_ui)
        pipeline.run(pts.human_prompt)


if __name__ == '__main__':
    app = App()
    app.initiate_ui()
    app.start()