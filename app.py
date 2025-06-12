import os
from dotenv import load_dotenv

from langchain import hub
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

# 문서 로드, 자르기
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pinecone import Pinecone
import streamlit as st
from langchain_pinecone import PineconeVectorStore
from llm import get_ai_message

# 터미널에서 streamlit run app.py

st.set_page_config(
    page_title="소득세 챗봇",
    page_icon=":guardsman:",        # 이모지 아이콘
    layout="wide",      # 레이아웃 설정
    initial_sidebar_state="expanded"        # 사이드바 초기상태
)

st.title("stream 기본 예제")
st.caption("소득세에 관련된 모든 것을 답변해드립니다.")

load_dotenv()

# pinecone data 로딩
index_name = 'tax-index'
pinecone_api_key = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_api_key)

if "message_list" not in st.session_state :
    st.session_state.message_list = []

# 전체 출력 ( message_list[-5:] 하면 최근 5개까지만, reversed : 최근이 맨 위)
for message in st.session_state.message_list :
    with st.chat_message(message['role']) :
        st.write(message["content"])

if user_question := st.chat_input(placeholder="소득세에 관련 궁금한 내용을 말씀해 주세요.") :
    with st.chat_message("user") :
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question})

    with st.spinner("답변을 생성하는 중입니다.") :
        ai_response = get_ai_message(user_question)
        with st.chat_message('ai') :
            ai_message = st.write_stream(ai_response)        # ai_response가 iteratator이기 때문에, write_stream 사용
        st.session_state.message_list.append({"role": "ai", "content": ai_message})     # 문자열은 list에 넣기! (iter은 계속 값이 바껴서ㅠ)