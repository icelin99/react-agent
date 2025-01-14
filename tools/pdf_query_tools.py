from langchain_openai import ChatOpenAI
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from PyPDF2 import PdfReader
from langchain.agents import tool
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_llm():
    return ChatOpenAI(
        model="deepseek-chat",
        temperature=0, # 温度为0，输出最确定的结果，适合查询任务
        max_tokens=1024,
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        base_url="https://oneapi.deepwisdom.ai/v1/",
    )

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

@tool
def pdf_query(query: str) -> str:
    """使用语义搜索在民法典中查找相关条款，并返回匹配的内容"""
    llm = get_llm()
    embeddings = get_embeddings()
    
    try:
        db = FAISS.load_local("db/faiss_index_constitution",
                              embeddings,
                              allow_dangerous_deserialization=True)
        print("---db finished loading: ", db)
    except:
        reader = PdfReader("tools/data/民法典.pdf")
        raw_text = ""
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                raw_text += text
        text_splitter = RecursiveCharacterTextSplitter(
            # separator="\n",
            chunk_size=1000, # 每个文本块1000字符
            chunk_overlap=500, # 重叠500字符，重叠率50%
        )
        texts = text_splitter.split_text(raw_text)
        # print("texts: ", texts)

        # create vector store
        db = FAISS.from_texts(texts, embeddings)
        db.save_local("db/faiss_index_constitution")
        print("---db finished saving: ", db)
    
    retriver = db.as_retriever(k=4) # 检索4个最相关的文本块
    result = retriver.invoke(query)

    return result

