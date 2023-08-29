# VirtualCorp

VirtualCorp aims to create fully working online business where employees can be humans or virtual agent.
The goal of the company is to fulfill customers' expectations by achieving `high level` tasks that requires
collaboration between the employees and the client.

In order to achieve a task requested by the customer, the system runs through a process assimilated as a
`pipeline` of `interactions`. It is a collaborative process between different agents and the customer is 
one of them. The interaction is subject to a contract describing the obligations of each participant in the
interaction and also their expectations. The role of the contract is to decide if the expected interaction
is fulfilled or not.

# How it works:

## The process

- The `system` initiates the process with a first interaction between the `customer` and an `ai agent`.
- The `ai agent` starts by rephrasing the `customer`'s expectations until the `customer` agrees with it.
- After the agreement, the system runs through several `interactions` involving each 2 well determined `agents`.
- Each `agent` needs to fulfill a `contract` supervised by the `system`.
- The `contracts` are defined between `agents` and the company *Virtual Corp* and determine possible `interactions`
and how they should be handled by either parties.

## Building blocs
- The `System`:
  1. It is unique and is the supervisor of all the agents, pipelines and interactions.
  2. It initialize a `pipeline` to handle **one** customer's expectation.
- A `Pipeline`:
  1. It is chain of defined `Contracts` required to fulfill the customer's expectation.
  2. When the pipeline is executed, it runs through each contract.
  3. For each contract, it starts the interaction.
  4. Then it checks the messages before sending them to the receiving party.
  5. it will wait until 
- A `Contract`:
  1. It involves 2 parties: `First` and `Second` qui sont deux `Agents`.
  2. It defines the `Rules` based on the `Prompts` of both parties.
  3. If the `Rules` are **not** fulfilled by the `Message`, it is set `To Revise`.
  4. The `Message` passed back to the sender to revise it (loop to 3.).
  5. The sender receives a log explaining why the `Message` was rejected.
  6. If all the `Rules` are fulfilled by the `Message`, it is `Released` and passed to the receiver.
  7. The interaction stops.
- A `Rule`:
  1. It can be of 2 types: `Compliance` and `Termination`.
  2. `Compliance`: It is a condition that should be fulfilled by a message to be `Accepted`.
  3. `Termination`: It is a condition to decide if the interactions end or not.
- An `Agent`:
  1. It can be `HUMAN` (requiring human input) or `VIRTUAL` (AI based).
  2. It receives an intial `Prompt`
  3. It outputs a `Message`.
- A `Prompt`:
  1. It defines what the `Agent` should handle as instructions.
  2. It containes placeholders for `Inputs`.
- A `Message`:
  1. It is the output of the agent
  2. If it is `HUMAN`, it is the manual answer to the prompt on the screen
  3. If it is a `VIRTUAL`, it is the predicted response from the Language Model.
  4. The message lifecycle
    1. `Created`
    2. `Rejected`
    3. `Accepted`


