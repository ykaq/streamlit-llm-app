# streamlit_app.py
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (ChatPromptTemplate,
                                    SystemMessagePromptTemplate,
                                    HumanMessagePromptTemplate)

# .env から OPENAI_API_KEY=sk-... を取得
load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

SYSTEM_MESSAGES = {
    "ITセキュリティ": "あなたはITセキュリティの専門家です。質問に対してセキュリティの観点から詳細かつ正確に回答してください。",
    "金融市場":     "あなたは金融市場の専門家です。経済動向、投資戦略、市場分析について専門的な見地から回答してください。",
    "健康と栄養":   "あなたは健康と栄養の専門家です。最新の科学的根拠に基づいた健康情報や栄養に関するアドバイスを提供してください。"
}

def get_llm_response(text: str, expert: str) -> str:
    system_tmpl = SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGES[expert])
    human_tmpl  = HumanMessagePromptTemplate.from_template("{text}")
    prompt      = ChatPromptTemplate.from_messages([system_tmpl, human_tmpl])
    chain       = prompt | llm
    return chain.invoke({"text": text}).content

# ---------- ここから Streamlit 画面 ----------
st.title("LLM 専門家チャット")

expert = st.selectbox("専門家を選んでください", list(SYSTEM_MESSAGES.keys()))
question = st.text_area("質問を入力してください")

if st.button("送信") and question:
    with st.spinner("考え中..."):
        answer = get_llm_response(question, expert)
    st.markdown("### 回答")
    st.write(answer)