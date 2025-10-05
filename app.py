from dotenv import load_dotenv
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# === 1. 環境変数設定 ===
# .env が存在すれば読み込む（ローカル実行用）
load_dotenv()

# Streamlit Cloud の Secrets にある場合はこちらも利用
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", "")

# デバッグ用表示（あとで削除OK）
if st.secrets.get("OPENAI_API_KEY"):
    st.caption("✅ Streamlit secrets loaded")
elif os.getenv("OPENAI_API_KEY"):
    st.caption("✅ .env file loaded")
else:
    st.error("❌ OPENAI_API_KEY が読み込まれていません。")

# === 2. LLM関数 ===
def get_llm_response(expert_type, user_input):
    if expert_type == "英語教師":
        system_message = "あなたは優秀な英語教師です。英語学習者にわかりやすく説明してください。"
    elif expert_type == "栄養士":
        system_message = "あなたは専門知識豊富な栄養士です。健康や食事に関する質問に丁寧に答えてください。"
    else:
        system_message = "あなたは親切なAIアシスタントです。質問に丁寧に答えてください。"

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{question}")
    ])
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run({"question": user_input})
    return result


# === 3. Streamlit UI ===
st.title("💬 LangChain × Streamlit デモアプリ")

st.write("""
### 🧭 アプリ概要
このアプリでは、選択した専門家（英語教師 or 栄養士）としてAIが回答します。
""")

expert_type = st.radio("AIの専門家タイプを選んでください：", ["英語教師", "栄養士"])
user_input = st.text_area("質問や相談内容を入力してください：")

if st.button("送信"):
    if user_input:
        with st.spinner("AIが考えています..."):
            answer = get_llm_response(expert_type, user_input)
        st.success("AIの回答：")
        st.write(answer)
    else:
        st.warning("テキストを入力してください。")
