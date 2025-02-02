from llama_index.core import VectorStoreIndex, \
    SimpleDirectoryReader, load_index_from_storage, \
    StorageContext
from llama_index.core.settings import Settings
from llama_index.llms.openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os

def initialize_index():
    # .env 파일에서 OpenAI API 키 로드
    load_dotenv()
    
    # LLM 모델 설정
    llm = OpenAI(
        model="gpt-3.5-turbo",
        temperature=0.1,
        max_tokens=512
    )
    
    # 전역 설정 업데이트
    Settings.llm = llm
    
    # VectorDB 저장 폴더 위치 설정
    vector_db_path = "./vector_db"
    
    # 문서 저장 위치 설정
    documents_path = "./documents"
    
    # 벡터 저장소 초기화
    if os.path.exists(vector_db_path):
        print("Loading existing index...")
        storage_context = StorageContext.from_defaults(persist_dir=vector_db_path)
        index = load_index_from_storage(storage_context)
    else:
        print("Creating new index...")
        reader = SimpleDirectoryReader(documents_path)
        documents = reader.load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=vector_db_path)
    
    return index

def main():
    st.title("문서 기반 Q&A 챗봇")
    
    # 인덱스 초기화
    index = initialize_index()
    
    # 채팅 엔진 생성
    chat_engine = index.as_chat_engine(
        verbose=True,
        streaming=True,
        system_prompt="당신은 친절한 AI 어시스턴트입니다. 주어진 문서를 기반으로 정확하게 답변해주세요."

    )

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("질문을 입력하세요"):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 어시스턴트 응답 생성
        with st.chat_message("assistant"):
            response = chat_engine.chat(prompt)
            st.markdown(response.response)
            st.session_state.messages.append({"role": "assistant", "content": response.response})

if __name__ == "__main__":
    main()