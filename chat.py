import os
os.environ["GROQ_API_KEY"]="GROQ_API_KEY"
from groq import Groq

from Agent import Agent
from Tools import Finish, AskUser, FetchPaper, Parse, AskExpert

client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
    )

agent = Agent(
    client=client,
    model="llama3-70b-8192",
    tools=[
        Finish(),
        AskExpert(),
        FetchPaper(),
        Parse(),
    ],
    max_steps=10,
)
