import streamlit as st
import ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

model = Ollama(model='deepseek-r1:1.5b')

with st.sidebar:
    st.title('Ollama with Langchain')
    st.header('DeepSeek Model')
    st.code('Model = deepseek-r1:1.5b')

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 AI Chatbot")
st.write("Chat with an **Ollama-powered AI** below!")

for role, text in st.session_state.messages:
    if role == "User":
        st.code(text, language="plaintext")
    else:
        with st.expander("🤖 Bot Reply", expanded=True):
            st.write(text)

user_input = st.text_input("Type your message...", key="user_input")

if st.button("Send"):
    if user_input.strip():
        st.session_state.messages.append(("User", user_input))

        template = """You are an expert research assistant. Use the provided context to answer the query. 
                      Be concise and factual (max 3 sentences)."""
        prompt = ChatPromptTemplate.from_template(template)

        chain = prompt | model
        bot_reply = chain.invoke({"question": user_input})

        st.session_state.messages.append(("Bot", bot_reply))

