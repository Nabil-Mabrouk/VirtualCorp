"""The idea is to queue the contracts in a pipeline and execute them one by one."""


class Entry():
    def __init__(self, contract, input=None):
        self.contract=contract
        self.input=input
        self.output=None
    
    def run(self):
        self.output=self.contract.run(self.input) 
        return self.output
    
    def __str__(self) -> str:
        return f"Entry contract: {self.contract}\n" \
               f"\tinput: {self.input}\n" \
               f"\toutput: {self.output}\n"

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
        last_output=first_input
        for entry in self.pipeline:
            entry.input=last_output
            last_output=entry.run()
            
    def __str__(self) -> str:
        return f"Pipeline name: {self.name}\n" \
               f"Pipeline length: {len(self.pipeline)}\n" \
               f"Pipeline entries: {self.pipeline}\n"
