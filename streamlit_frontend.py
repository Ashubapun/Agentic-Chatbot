import streamlit as st
from backend import bot
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

CONFIG = {"configurable" : {"thread_id" : "thread-1"}}

# st.session_state -> dict -> 
# creating session_state to store the history of messages
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

# loading the message history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])


user_input = st.chat_input("Type here ")

if user_input:

    # first add the message to message_history
    st.session_state["message_history"].append({"role" : "user", "content" : user_input})
    with st.chat_message("user"):
        st.text(user_input)
    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in bot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= {'configurable': {'thread_id': 'thread-1'}},
                stream_mode= 'messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})