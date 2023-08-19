# VirtualCorp

VirtualCorp aims to create fully working online business where all employees are virtual agent
How it works:
Step 1: business idea validation
- The process starts by a prompt introduced by the client (Human) about a busines process idea that he would like to automate
- A first welcome agent interacts with the client to rephrase the business idea and make sure that is not illegal
- If the welcome agent and the Human reach an agreement on the business idea, then a trigger is sent and the process go to step 2

> ** note **
>- input: Human business idea
>- output: rephrased business idea
>- contract: welcome agent and Human reach an agreement 

Step 2: Business plan
- The step 2 is triggered by the smart contract of step 1 (inpout rephrased business idea)
- The step 2 aim to develop a simple business plan (output business plan)
- The business plan is proposed business plan agent and validated by the user
- The business plan agent recieves this system prompt:
> You role is crafting a comprehensive business plan for my innovative venture. This business aims to **\[rephrased business idea\]**. The plan should encompass key elements such as market research, target audience identification, unique value proposition, technology integration, data privacy and security measures, monetization strategy, customer acquisition and marketing approaches, operational plan highlighting \[AI-driven customer support or any relevant specifics\], scalability tactics, financial projections considering user growth, system maintenance costs, and profitability estimations, as well as a forward-looking long-term vision. Please ensure each stage receives my approval before proceeding to the next.
> Tools: Business plan agent should be allowed to use a google search tool to get market data [https://www.polarismarketresearch.com/](https://www.polarismarketresearch.com/)

> ** note **
>- input: rephrased business idea
>- output: business plan
>- contract: Human and busines plan agent agree on the business plan. The business plan is still legal. The business plan adress the following sections: target audience, value proposition, monetezation strategy, customer acquisition and marketing strategy, financial projections, profitability estimation

Step 3: Business process design
- The step 3 is triggered by the smart contract of step 2
- Step 3 aims to provide a detailed description of the business process (output business process description)
- The business process is proposed by the agent : Business process expert and validated by the client
The business process agent recieves this system prompt:
> I will provide you with a business plan for a fully automated **\[rephrased business idea\]**. As a business process design expert, I need your assistance to define the automated processes required to achieve our objectives. Please ensure each process includes: inputs, outputs, tasks, actors, resources, data and data flow, interactions with other processes, and KPIs. Wait for my approval before moving on to each subsequent process. Also, kindly remember to maintain the user's approval at each step

> ** Private note **
- input: Business plan and rephrased business idea
- output: detailed business process
- contract: business process agent and Human reach an agreement

Step 4: Business creation
Step 4 is an iterative step between two agents:
- task specifier agent who recieves as input the detailed description of the business process
- python programmer: who generates the code based on the instructions of the task specifier

> ** note **
>- input: Human business idea
>- output: zip file with the business plan, the business process description and the code
>- contract: between two agents, each one should stick to his system prompt. Each message each checked before submission

