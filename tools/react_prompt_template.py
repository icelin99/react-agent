from langchain.prompts import PromptTemplate

def get_prompt_template():
    return PromptTemplate.from_template(
        """
        Answer the following question as best as you can. You have access to the following tools: 
        
        {tools}
        pdf_query: 输入问题，可以在民法典中搜索相关条款.

        请按照以下步骤回答问题：
        1. 使用 pdf_query 工具搜索相关法律条款
        2. 基于搜索到的条款内容给出专业解答
        3. 如果查询到的条款足以回答问题，请直接给出最终答案，并停止
        4. 如果查询不到相关条款，请说明原因并停止
        5. 不要重复调用工具，除非明确需要补充信息

        Use the following format:

        Question: the input question you must answer

        Thought: you should always think about what to do, you can just answer if the question is something basic and not fact-based.

        Action: the action to take, should be one of [{tool_names}]

        Action Input: [your input to the action]

        Observation: the result of the action

        Thought: I now know the final answer

        Final Answer: the final answer to the original input question, stop once you have found the answer!

        Begin!

        Question: {question}

        Thought: {agent_scratchpad}
        """
    )