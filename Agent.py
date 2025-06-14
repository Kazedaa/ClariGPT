import instructor
from pydantic import BaseModel

from prompts import DEFAULT_PROMPT, SYSTEM_PROMPT


logs = open("logs.txt",'w')

class ReACT(BaseModel):
    thought : str
    action : str
    action_input : str

class Structurize():
    def __init__(self,client, model):
        self.patched_client = instructor.from_groq(client)
        self.model = model
        
    def __call__(self, messages):
        reply = self.patched_client.chat.completions.create(
            model = self.model,
            response_model = ReACT,
            messages = [{"role": "user", "content": f"Extract: {messages}"}],
        )
        return reply

class Agent():
    def __init__(self, client, model, tools, max_steps=10):
        self.client = client
        self.max_steps = max_steps
        self.model = model
        self.history = []
        self.tools = tools
        self.structurizer = Structurize(client, model)
        
    def __call__(self, message):
        for i in range(self.max_steps):
            response = self.run(message)
            action = next((tool for tool in self.tools if response.action==tool.__class__.__name__.lower()),None)
            if action is None:
                print(f"THOUGHT : {response.thought}\n\nACTION : {response.action}\n\nACTION INPUT : {response.action_input}",file=logs,flush=True)
                print(f"Action {response.action} not found in tools.")
                print(f"Action {response.action} not found in tools.",file=logs,flush=True)
                self.history.append(f"THOUGHT : {response.thought}\n\nACTION : {response.action}\n\nACTION INPUT : {response.action_input}")
                break
            observation = action.run(response.action_input)
            self.history.append(f"THOUGHT : {response.thought}\n\nACTION : {response.action}\n\nACTION INPUT : {response}\n\nOBSERVATION : {observation}")
            print(f"THOUGHT : {response.thought}\n\nACTION : {response.action}\n\nACTION INPUT : {response.action_input}\n\nOBSERVATION : {observation}",file=logs,flush=True)
            if response.action.lower() == "finish":
                print("Finished.",file=logs,flush=True)
                return observation
            
    def get_tool_desc(self):
        return  "\n".join([f"{tool.__class__.__name__.lower()}: {tool.run.__doc__}" for tool in self.tools])
    
    def run(self, query, max_retries=3):
        for i in range(max_retries):
            try:
                prompt = DEFAULT_PROMPT.format(query=query, history=self.history, tool_descriptions=self.get_tool_desc())
                output = self.client.chat.completions.create(
                        messages=[
                            {
                                "role": "system",
                                "content": SYSTEM_PROMPT,
                            },
                            {
                                "role": "user",
                                "content": prompt,
                            },
                            
                        ],
                        model=self.model,
                    ).choices[0].message.content
                response = self.structurizer(output)
                return response
                        
            except Exception as e:
                print(e)
                print(e,file=logs,flush=True)
                print("Retrying...")
                print("Retrying...",file=logs,flush=True)
                continue
        print("Max retries exceeded.")
        print("Max retries exceeded.",file=logs,flush=True)
        return ReACT(
            thought="",
            action="finish",
            action_input=""
            )
        