
from logger_config import logger
import streamlit as st

class Pipeline:
    """
    Represents a data processing pipeline that executes a series of contracts sequentially.

    Attributes:
        name (str): The name of the pipeline.
        contracts (list): A list of contract objects to be executed in the pipeline.
        ui (object, optional): An optional user interface object for interaction (default is None).
    """
    def __init__(self, name, contracts, ui=False):
        """
        Initializes a new Pipeline instance.

        Args:
            name (str): The name of the pipeline.
            contracts (list): A list of contract objects to be executed in the pipeline.
            ui (object, optional): An optional user interface object for interaction (default is False).
        """
        self.name = name
        self.contracts = contracts
        self.ui=ui

    def run(self, input):
        """
        Executes the pipeline on the given input data.

        Args:
            input (str): The input data (must be a string) to be processed by the pipeline.

        Returns:
            str: The processed output data (string) after executing all contracts in the pipeline.

        Raises:
            ValueError: If the input is not a string.
        """
        if not isinstance(input, str):
            logger.error(f"[Pipeline {self.name}]: input must be a string - Actual input : {input}")
            raise ValueError("Input must be a string.")
        output = input
        for contract in self.contracts:
            try:
                logger.debug(f"[Pipeline: {self.name}] Running contract: {contract.name}")
                #if self.ui: st.warning("Starting pipeline {self.name} ...")
                output = contract.run(output)
                logger.debug(f"[Pipeline: {self.name}] Terminated contract {contract.name} with the following output: {output}")
            except Exception as e:
                logger.warning(f"[Pipeline: {self.name}] Contract : {contract.name} encountered an error: {str(e)}\n {input} \n {output}")
                break
        return output

