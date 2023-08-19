# l'idée est de lier les contrats entre eux pour dire qui s'éxécute en premier


class Entry():
    def __inti__(self, contract, input, output):
        self.contract=contract
        self.input=input # l'output du contrat précédent
        self.output=output # l'input du contrat suivant
    
    def run(self):
        self.output=self.contract.run(self.input) 
        return self.output


class Pipeline():
    def __inti__(self, name="pipeline"):
        self.name=name
        self.pipeline=[]
    
    def add(self, contract, input, output):
        self.pipeline.append(Entry(contract, input, output))

    def execute(self, first_input):
        last_output=first_input
        for entry in self.pipeline:
            entry.input=last_output
            last_output=entry.run()
