import streamlit as st
from openai import OpenAI
from streamlit import secrets

# 设置页面标题
st.title("💬 DeepSeek Chatbot")

# 在侧边栏添加配置选项
with st.sidebar:
    # 提供一个文本输入框让用户可以手动输入API Key（可选）
    openai_api_key = st.text_input("DeepSeek API Key", key="chatbot_api_key", type="password")
    "[获取 DeepSeek API key](https://platform.deepseek.com/api_keys)"
    if st.button("开启新对话"):
        if "messages" in st.session_state and len(st.session_state.messages) > 0:
            # 保存当前对话到历史对话列表
            if "history_conversations" not in st.session_state:
                st.session_state.history_conversations = []
            st.session_state.history_conversations.append(st.session_state.messages)
            st.session_state.messages = [{"role": "assistant", "content": "欢迎使用对话机器人，你想知道什么?"}]

            # 显示历史对话列表
    st.subheader("历史对话")
    if "history_conversations" in st.session_state:
        for idx, conv in enumerate(st.session_state.history_conversations):
            if st.button(f"对话 {idx + 1}", key=f"load_conv_{idx}"):
                st.session_state.messages = conv
                # st.success(f"成功加载对话 {idx + 1}")
# 如果用户没有提供API Key，则尝试从secrets.toml文件中获取
if not openai_api_key:
    try:
        openai_api_key = secrets.deepseek_api.key
    except AttributeError:
        pass  # 如果在secrets.toml中找不到API Key，则保持openai_api_key为空

# 检查API Key是否已提供
if not openai_api_key:
    st.info("请添加新的API Key")
else:
    base_url = "https://api.deepseek.com"
    client = OpenAI(api_key=openai_api_key, base_url=base_url)

    # 初始化对话历史记录
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "欢迎使用对话机器人，你想知道什么?"}]

        # 显示对话历史
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

        # 获取用户输入
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # 调用DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.messages,
            stream=False
        )
        assistant_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        st.chat_message("assistant").write(assistant_reply)
