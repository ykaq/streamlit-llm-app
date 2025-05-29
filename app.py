import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

import os
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"

# LLMの初期化
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def get_llm_response(text: str, expert_type: str) -> str:
    """
    入力テキストと専門家の種類を受け取り、LLMからの回答を返す関数。
    """
    system_messages = {
        "A": "あなたはITセキュリティの専門家です。質問に対してセキュリティの観点から詳細かつ正確に回答してください。",
        "B": "あなたは金融市場の専門家です。経済動向、投資戦略、市場分析について専門的な見地から回答してください。",
        "C": "あなたは健康と栄養の専門家です。最新の科学的根拠に基づいた健康情報や栄養に関するアドバイスを提供してください。"
    }

    system_message_template = SystemMessagePromptTemplate.from_template(
        system_messages.get(expert_type, "あなたは親切なアシスタントです。") # デフォルトメッセージ
    )
    human_message_template = HumanMessagePromptTemplate.from_template("{text}")

    chat_prompt = ChatPromptTemplate.from_messages([
        system_message_template,
        human_message_template,
    ])

    chain = chat_prompt | llm
    response = chain.invoke({"text": text})
    return response.content

def main():
    """
    コマンドラインインターフェースを実装したメイン関数。
    """
    print("--- LLM専門家チャット ---")
    print("以下の専門家から選択し、質問を入力してください。")
    print("A: ITセキュリティ")
    print("B: 金融市場")
    print("C: 健康と栄養")
    print("終了するには 'exit' と入力してください。")
    print("---")

    while True:
        expert_choice = input("専門家を選択してください (A/B/C): ").upper()
        if expert_choice == 'EXIT':
            break
        if expert_choice not in ["A", "B", "C"]:
            print("無効な選択です。A, B, C のいずれかを入力してください。")
            continue

        user_input = input("質問を入力してください: ")
        if user_input.lower() == 'exit':
            break

        print("\nLLMからの回答:")
        response = get_llm_response(user_input, expert_choice)
        print(response)
        print("\n---")

if __name__ == "__main__":
    main()