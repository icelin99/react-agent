import streamlit as st
from agent import Agent
import os
from langchain_core.messages import HumanMessage, AIMessage
import sys

import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

agent = Agent()

# create a streamlit app
st.set_page_config(
    page_title="lawyer-GPT⚖️",
    page_icon="🧑‍⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)
st.title("lawyer-GPT🧑‍⚖️")
initial_mgx = """
#### Welcome!!! I am your legal assistant chatbot🧑‍⚖️
#### You can ask me any queries about the law.
> NOTE: Currently I have only access to the 民法典. So try to ask relevant questions only😊.
"""
st.markdown(initial_mgx)
# use session state to store the chat history
if "store" not in st.session_state:
    st.session_state.store = []

store = st.session_state.store

for message in store:
    if message.type == "ai":
        avatar = "🧑‍⚖️"
    else:
        avatar = "👤"
    with st.chat_message(message.type,avatar=avatar):
        st.markdown(message.content)

# ReAct to user input
if prompt := st.chat_input("Enter your question"):
    print("prompt:", prompt)
    # display message
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.chat_message("assistant", avatar="🧑‍⚖️").markdown("Thinking...")
    prompt += "请用中文回答"

    store.append(HumanMessage(content=prompt))
    sys.stdout.flush()
    try:
        # 获取agent的响应
        response_data = agent.ask(HumanMessage(content=prompt))
        sys.stdout.flush()
        print("Agent响应:")
        print("Observation=:", response_data['observation'])
        print("Thought=:", response_data['thought'])
        print("Answer=:", response_data['final_answer'])
        if response_data['final_answer']:
            final_answer = response_data['final_answer'].replace(
                "For troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE", 
                ""
            ).strip()
        
        # 显示思考过程
        st.chat_message("assistant", avatar="🧑‍⚖️").markdown("**搜索结果:**\n" + response_data['observation'])
        st.chat_message("assistant", avatar="🧑‍⚖️").markdown("**思考:**\n" + response_data['thought'])
        
        # 显示最终答案
        st.chat_message("assistant", avatar="🧑‍⚖️").markdown("**最终答案:**\n" + final_answer)
        
        # 存储到聊天历史
        response = AIMessage(content=response_data['final_answer'])
    except:
        response = AIMessage(content="Sorry, I am not able to answer this question. Please try again later.")
    
    store.append(response)
    # # display response
    # st.chat_message("assistant", avatar="🧑‍⚖️").markdown(response.content)



