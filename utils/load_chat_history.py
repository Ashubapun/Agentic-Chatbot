import streamlit as st
from backend import bot

def load_chat(thread_id):
    return bot.get_state(config={'configurable' : {"thread_id" : thread_id}}).values["messages"]