# =============================================
# 💬 LangChain × Streamlit デモアプリ（完全版）
# =============================================

# === 0. インポート ===
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import openai  # 接続テスト用

# === 1. 環境変数設定 ===
# ローカル用: .env ファイルを読み込む（あれば）
load_dotenv()

# Streamlit Cloud用: Secretsから読み込む
if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"]:
    os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", "")

# === APIキー確認（サイドバー表示） ===
st.sidebar.header("🔐 API Key チェック")
api_key = os.getenv("OPENAI_API_KEY", "")

if api_key and api_key.startswith("sk-"):
    st.sidebar.success("✅ APIキーが認識されました")
    st.sidebar.caption(f"Key prefix: {api_key[:8]}******")
else:
    st.sidebar.error("❌ OPENAI_API_KEY が設定されていません")
    st.sidebar.caption("Secrets または .env を確認してください。")
    st.stop()

# OpenAI SDKにもキーを明示的に渡す
openai.api_key = api_key

# === 1.5 OpenAI API接続テスト ===
st.sidebar.markdown("---")
st.sidebar.subheader("🧩 OpenAI 接続テスト")
try:
    client = openai.OpenAI(api_key=api_key)
    models = client.models.list()
    st.sidebar.success("✅ OpenAI API 接続成功！")
    st.sidebar.caption(f"利用可能モデル数: {len(models.data)}")
except Exception as e:
    st.sidebar.error(f"❌ API接続エラー: {e}")
    st.stop()


# === 2. LLM応答関数 ===
def get_llm_response(expert_type, user_input):
    """専門家タイプと入力内容をもとにLLMの回答を返す関数"""

    # システムメッセージを選択
    if expert_type == "英語教師":
        system_message = "あなたは優秀な英語教師です。英語学習者にわかりやすく説明してください。"
    elif expert_type == "栄養士":
        system_message = "あなたは専門知識豊富な栄養士です。健康や食事に関する質問に丁寧に答えてください。"
    else:
        system_message = "あなたは親切なAIアシスタントです。質問に丁寧に答えてください。"

    # LangChain設定
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
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

### 🪄 操作手順
1. 専門家タイプを選択  
2. テキストを入力  
3. 「送信」ボタンをクリック！
""")

# 専門家タイプ選択
expert_type = st.radio("AIの専門家タイプを選んでください：", ["英語教師", "栄養士"])

# 質問入力欄
user_input = st.text_area("質問や相談内容を入力してください：")

# 実行ボタン
if st.button("送信"):
    if user_input.strip():
        with st.spinner("AIが考えています..."):
            answer = get_llm_response(expert_type, user_input)
        st.success("AIの回答：")
        st.write(answer)
    else:
        st.warning("テキストを入力してください。")
