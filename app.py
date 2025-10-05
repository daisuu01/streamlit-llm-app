from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI   # ✅ ← ここを修正
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# === 関数定義 ===
def get_llm_response(expert_type, user_input):
    """専門家タイプと入力内容をもとにLLMの回答を返す関数"""

    # システムメッセージを選択
    if expert_type == "英語教師":
        system_message = "あなたは優秀な英語教師です。英語学習者にわかりやすく説明してください。"
    elif expert_type == "栄養士":
        system_message = "あなたは専門知識豊富な栄養士です。健康や食事に関する質問に丁寧に答えてください。"
    else:
        system_message = "あなたは親切なAIアシスタントです。質問に丁寧に答えてください。"

    # LangChainの設定
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{question}")
    ])

    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run({"question": user_input})
    return result


# === Streamlit UI ===
st.title("💬 LangChain × Streamlit デモアプリ")
st.write("""
### 🧭 アプリ概要
このアプリでは、選択した専門家（英語教師 or 栄養士）としてAIが回答します。
テキストを入力して「送信」ボタンを押すと、AIの回答が表示されます。

### 🪄 操作手順
1. 専門家タイプを選択してください  
2. テキストを入力してください  
3. 「送信」ボタンをクリックするとAIが回答します
""")

# 専門家選択
expert_type = st.radio("AIの専門家タイプを選んでください：", ["英語教師", "栄養士"])

# 入力フォーム
user_input = st.text_area("質問や相談内容を入力してください：")

# 実行ボタン
if st.button("送信"):
    if user_input:
        with st.spinner("AIが考えています..."):
            answer = get_llm_response(expert_type, user_input)
        st.success("AIの回答：")
        st.write(answer)
    else:
        st.warning("テキストを入力してください。")
