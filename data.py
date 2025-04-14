import streamlit as st
st.title('Hello, Streamlit!')
prompt = st.chat_input('Enter your message')
# Below is partial code of D:/project/streamlit/venv/Lib/site-packages/streamlit/__init__.py:
if prompt:
    user_message = st.chat_message(f'You said: {prompt}')
    user_message.write(f'You said: {prompt}')

    ai_message = st.chat_message('I am a chatbot. How can I help you?')
    ai_message.write('I am a chatbot. How can I help you?')

