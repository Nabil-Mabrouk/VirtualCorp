
from logger_config import logger

class Pipeline:
    def __init__(self, name, contracts):
        self.name = name
        self.contracts = contracts

    def run(self, input):
        output = input
        for contract in self.contracts:
            try:
                logger.info(f"[Pipeline: {self.name}] Running contract: {contract.name}")
                output = contract.run(output)
            except Exception as e:
                logger.warning(f"[Pipeline: {self.name}] Contract : {contract.name} encountered an error: {str(e)}")
                break
        return output

