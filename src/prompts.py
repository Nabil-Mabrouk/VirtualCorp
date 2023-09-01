human_prompt = "Provide a business idea that comply with the following rules:\n \
                1- You business idea must be legal\n \
                2- You business idea must be ethical\n"

contract_prompt = '''Please evaluate the following business idea \n\n '<QUERY>'\n\n based on the following criteria:\n\n 
                '<RULES>' \n\n
                Classify the business idea as one of the following:\n
                'Compliant' if it meets all criteria.\n
                'Non compliant' if it violates any of the criteria.\n
                'Neutral' if there is not enough information to determine.\n\n
                 Your answer should follow this format\n\n 
                '{"Answer": "### your answer (Compliant, Non compliant or Neutral)",
                    "Reasoning": "### your resoning process to come to this answer"
                }'\n\n 
                '''

agent_prompt = '''You will recieve a message with a business idea. Your role is to rephrase it and provide more details\
                You will also receive a feedback on your last message and your last message if any. 
                You should take into consideration the feedback if any. 
                You rephrased idea must comply with the following rules: \n\n\
                1- You business idea must be legal \n\
                2- You business idea must be ethical \n\n \
                Message: <MESSAGE>\n\n\
                Feedback: <FEEDBACK> \n\n\
                Your last message: <LAST_MESSAGE> \n\n\
 
                Your answer must follow this format\n\n \
                '{"Answer": "### your answer (Rephrased business idea)"}'\n\n 
                Always answer according to this format. Do not add anything elese to your answer.\n'''