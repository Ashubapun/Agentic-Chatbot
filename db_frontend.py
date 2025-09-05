import streamlit as st
from db_backend import bot
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
import uuid
from utils.generate_thread import generate_thread_id
from utils.generate_new_chat import new_chat
from utils.add_threads import add_thread_id
from utils.load_chat_history import load_chat
from utils.retrieve_threads import retrieve_all_threads


# st.session_state -> dict -> 
# creating session_state to store the history of messages
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()


if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_thread_id(st.session_state["thread_id"])


# ------------------------------------------------------------

CONFIG = {"configurable" : {"thread_id" : st.session_state["thread_id"]}}

# ----------------- SIDEBAR UI --------------------------------
 
st.sidebar.title("Agentic Chatbot 🤖")

if st.sidebar.button("New Chat"):
    new_chat()

st.sidebar.header("Chats")

for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = load_chat(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages

# ----------------- MAIN UI ----------------------------------

# loading the message history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])



user_input = st.chat_input("Ask Anything ")

if user_input:

    # first add the message to message_history
    st.session_state["message_history"].append({"role" : "user", "content" : user_input})
    with st.chat_message("user"):
        st.text(user_input)
    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in bot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})