from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AgentAction
import os
from datetime import datetime
import pytz
from tools.pdf_query_tools import pdf_query
from tools.react_prompt_template import get_prompt_template
from langchain.agents import AgentExecutor, create_react_agent
import warnings
import re

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
        tools = [pdf_query]
        prompt_template = get_prompt_template()
        agent = create_react_agent(
            self.llm,
            tools,
            prompt_template
        )
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_execution_time=60,
            early_stopping_method="force",  # 添加早停方法
            return_intermediate_steps=True  # 返回中间步骤
        )
        if isinstance(message, list) and len(message) > 0:
            question = message[0].content
        else:
            question = message.content
        print(f"---messages: {question}")
        
        try:
            result = agent_executor.invoke({
                "input": self.get_prefix(),
                "question": question
            })
            
            # 格式化输出结果
            print("\n=== 法律依据 ===")
            intermediate_steps = result.get("intermediate_steps", [])
            last_action = intermediate_steps[-1][0]
            print(f"-----last_log: {last_action}")
            if isinstance(last_action, AgentAction) and hasattr(last_action, 'log'):
                last_log = last_action.log
            else:
                raise ValueError("Invalid input: last_action is not an AgentAction object or missing 'log' attribute.")
            

            # 提取 Observation
            observation_match = re.search(r"Observation:\s*(.*?)(Thought:|$)", last_log, re.S)
            observation = observation_match.group(1).strip() if observation_match else None

            # 提取 Thought
            thought_match = re.search(r"Thought:\s*(.*?)(Final Answer:|$)", last_log, re.S)
            thought = thought_match.group(1).strip() if thought_match else None
            # 提取 Final Answer
            final_answer_match = re.search(r"Final Answer:\s*(.*)", last_log, re.S)
            final_answer = final_answer_match.group(1).strip() if final_answer_match else None

            print("=== 中间步骤 ===")
            print(f"Observation: {observation}")
            print(f"Thought: {thought}")
            print(f"Final Answer: {final_answer}")
   
            print("\n=== 最终答案 ===")
            print(f"💡 {result}")
            
            # 返回结构化的结果
            return {
                "intermediate_steps": intermediate_steps,
                "observation": observation,
                "thought": thought,
                "final_answer": final_answer
            }
            
        except Exception as e:
            print(f"\n=== 执行出错 ===")
            print(f"错误类型: {type(e).__name__}")
            print(f"错误信息: {str(e)}")
            raise
            
    

if __name__ == "__main__":
    agent = Agent()
    message = [HumanMessage(content="你懂租房合同吗？")]

    response = agent.ask(message)

    print("===main===")
    print(response)
