from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, AIMessage

from src.model.agent import State
from src.agent.llm import llm_topic_checker
from src.agent.prompt import isCheeseChat

def topic_checker(state: State, config: RunnableConfig):
    print("=" * 10 + "topic_checker" + "=" * 10)

    result = llm_topic_checker.invoke([SystemMessage(content=isCheeseChat)] + state["messages"], config)

    return {"is_topic": result["result"]}

def general_chatbot(state: State, config: RunnableConfig):
    print("general_chatbot")
    return {}

def reasoner(state: State, config: RunnableConfig):
    print("reasoner")
    return {}

def history_filter(state: State, config: RunnableConfig):
    print("history_filter")
    return {}

context_collector = ToolNode([])

def final_chatbot(state: State, config: RunnableConfig):
    print("final_chatbot")
    return {}

def ask_more(state: State, config: RunnableConfig):
    print("ask_more")
    return {}

def request_query(state: State, config: RunnableConfig):
    print("request_query")
    return {}

def feedback(state: State, config: RunnableConfig):
    print("feedback")
    return {}

