from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode

from src.model.agent import State

def topic_checker(state: State, config: RunnableConfig):
    return {}

def general_chatbot(state: State, config: RunnableConfig):
    return {}

def reasoner(state: State, config: RunnableConfig):
    return {}

def history_filter(state: State, config: RunnableConfig):
    return {}

context_collector = ToolNode([])

def final_chatbot(state: State, config: RunnableConfig):
    return {}

def ask_more(state: State, config: RunnableConfig):
    return {}

def request_query(state: State, config: RunnableConfig):
    return {}

