import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import Agent
from langchain.schema import HumanMessage

agent = Agent()

message = [HumanMessage(content="你懂租房合同吗？")]

response = agent.ask(message)

print("===main===")
print(response)