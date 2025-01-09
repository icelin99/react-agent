from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from datetime import datetime
import pytz

class Agent:
    name = "Agent"
    llm = None
    model = "claude-3-5-sonnet-20240620"

    def __init__(self):
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0,
            max_tokens=1024,
            timeout=10,
            max_retries=2,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            base_url="https://oneapi.deepwisdom.ai/v1/",
        )

    def get_prefix(self):
        time_zone = pytz.timezone('Asia/Shanghai')
        current_time = datetime.now(time_zone)
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"The current time is {formatted_time}. You are {self.name}, a helpful lawyer assistant."

    def ask(self, message):
        messages = [
            SystemMessage(content=self.get_prefix()),
            *message
        ]
        print(f"input messages: {messages}")
        return self.llm.invoke(messages)
    

if __name__ == "__main__":
    agent = Agent()
    message = [HumanMessage(content="What is LLM Agent? When is today")]

    response = agent.ask(message)

    print(response.content)
