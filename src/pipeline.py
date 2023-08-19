"""The idea is to queue the contracts in a pipeline and execute them one by one."""


class Entry():
    def __init__(self, contract, input=None):
        self.contract=contract
        self.input=input # l'output du contrat précédent
        # self.output=output # l'input du contrat suivant
        self.output=None
    
    def run(self):
        self.output=self.contract.run(self.input) 
        return self.output
    
    def __str__(self) -> str:
        return str(self.contract) + " with input: " + str(self.input) + " and output: " + str(self.output)


class Pipeline():
    def __init__(self, name="pipeline"):
        self.name=name
        self.pipeline=[]
    
    def add(self, contract, input=None, output=None):
        self.pipeline.append(Entry(contract, input, output))

    def execute(self, first_input):
        """Sequentially executes the piped contracts.

        Args:
            first_input (string): The first input for the first contract in the pipeline.
        """
        last_output=first_input
        for entry in self.pipeline:
            entry.input=last_output
            last_output=entry.run()
