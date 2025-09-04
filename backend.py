import os
from typing import TypedDict, Annotated, List, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, END, MessagesState, START
from langgraph.prebuilt import ToolNode


from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# response = llm.invoke([HumanMessage(content="Hello, how are you?")])
# print(response.content)

#Define State
class State(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

# Chatbot Functionality
def chatbot(state: State):
    """You are an intelligent chatbot. you have to answer all the questions asked by user and if you don't know answer to any of the question then simply say that you don't know with an apology, don't make up things if you don't know."""

    messages = state["messages"]
    response = llm.invoke(messages)

    return {"messages":response}

# Use Persistance
checkpointer = InMemorySaver()

# Build StateGraph
graphbuilder = StateGraph(State)

# add nodes
graphbuilder.add_node("chatbot", chatbot)

# add edges
graphbuilder.add_edge(START, "chatbot")
graphbuilder.add_edge("chatbot", END)

bot = graphbuilder.compile(checkpointer=checkpointer)


