import streamlit as st
from utils.generate_thread import generate_thread_id
from utils.add_threads import add_thread_id

def new_chat():
    thread_id = generate_thread_id()

    st.session_state["thread_id"] = thread_id
    add_thread_id(st.session_state["thread_id"])

    st.session_state["message_history"] = []