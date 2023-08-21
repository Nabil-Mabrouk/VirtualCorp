"""The idea is to queue the contracts in a pipeline and execute them one by one."""


class Entry():
    def __init__(self, contract, input=None):
        self.contract=contract
        self.input=input
        self.output_1=""
        self.output_2=""
    
    def run(self, input=""):
        self.input = input
        self.output_1, self.output_2 =self.contract.run(self.input)
    
    def __str__(self) -> str:
        return f"Entry contract: {self.contract}\n" \
               f"\tinput: {self.input}\n" \
               f"\toutput agent 1: {self.output_1}\n" \
               f"\toutput agent 2: {self.output_2}\n"

class Pipeline():
    def __init__(self, name="pipeline"):
        self.name=name
        self.pipeline=[]
    
    def add(self, contract, input=None):
        self.pipeline.append(Entry(contract, input))

    def execute(self, first_input):
        """Sequentially executes the piped contracts.

        Args:
            first_input (string): The first input for the first contract in the pipeline.
        """
        for entry in self.pipeline:
            entry.run(input=first_input)
            
    def __str__(self) -> str:
        return f"Pipeline name: {self.name}\n" \
               f"Pipeline length: {len(self.pipeline)}\n" \
               f"Pipeline entries: {self.pipeline}\n"
