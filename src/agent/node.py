from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from src.model.agent import State
from src.agent.llm import llm_topic_checker, llm_general_chatbot, llm_reasoner, llm_tools
from src.agent.prompt import isCheeseChat, general, reasoning, query2tool
from src.agent.tool import mongo_filter, mongo_aggregation, pinecone_search

def topic_checker(state: State, config: RunnableConfig):
    print("topic_checker" + "=" * 30)
    result = llm_topic_checker.invoke([SystemMessage(content=isCheeseChat)] + state["messages"], config)
    return {"messages": AIMessage(content=result["reason"]), "is_topic": result["result"]}

def general_chatbot(state: State, config: RunnableConfig):
    print("general_chatbot" + "=" * 30)
    result = llm_general_chatbot.invoke([SystemMessage(content=general)] + state["messages"], config)
    return {"messages": [result]}

def reasoner(state: State, config: RunnableConfig):
    print("reasoner" + "=" * 30)
    result = llm_reasoner.invoke([SystemMessage(content=reasoning)] + state["messages"], config)
    return {"messages": AIMessage(content=result["reason"]), "next_action": result["choice"]}

def history_filter(state: State, config: RunnableConfig):
    print("history_filter" + "=" * 30)
    return {}

def data_collector(state: State, config: RunnableConfig):
    print("data_collector" + "=" * 30)
    result = llm_tools.invoke([SystemMessage(content=query2tool)] + state["messages"], config)
    return {"messages": [result]}

tool_node = ToolNode([mongo_filter, mongo_aggregation, pinecone_search])

def final_chatbot(state: State, config: RunnableConfig):
    print("final_chatbot" + "=" * 30)
    return {}

def ask_more(state: State, config: RunnableConfig):
    print("ask_more" + "=" * 30)
    return {}

def request_query(state: State, config: RunnableConfig):
    print("request_query" + "=" * 30)
    return {}

def feedback(state: State, config: RunnableConfig):
    print("feedback" + "=" * 30)
    return {}

