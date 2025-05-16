from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from src.model.agent import State
from src.agent.llm import (
    llm_topic_checker,
    llm_general_chatbot,
    llm_reasoner,
    llm_tools,
    llm_final_chatbot,
    llm_history_filter
)
from src.agent.prompt import (
    isCheeseChat,
    general,
    reasoning,
    query2tool,
    system,
    history
)
from src.agent.tool import mongo_filter, mongo_aggregation, pinecone_search

def topic_checker(state: State, config: RunnableConfig):
    print("\n\ntopic_checker" + "=" * 30)
    result = llm_topic_checker.invoke([SystemMessage(content=isCheeseChat)] + state["messages"], config)
    return {"chat_history": [state["messages"][-1]], "messages": AIMessage(content=result["reason"]), "is_topic": result["result"]}

def general_chatbot(state: State, config: RunnableConfig):
    print("\n\ngeneral_chatbot" + "=" * 30)
    result = llm_general_chatbot.invoke([SystemMessage(content=general)] + state["messages"], config)
    return {"messages": [result], "chat_history": [result]}

def reasoner(state: State, config: RunnableConfig):
    print("\n\nreasoner" + "=" * 30)
    result = llm_reasoner.invoke([SystemMessage(content=reasoning)] + state["messages"], config)
    return {"messages": [AIMessage(content=result["reason"])], "next_action": result["choice"]}

def history_filter(state: State, config: RunnableConfig):
    print("\n\nhistory_filter" + "=" * 30)
    result = llm_history_filter.invoke([SystemMessage(content=history)] + state["messages"], config)
    print(result)
    return {"filtered_history": result["chat"]}

def data_collector(state: State, config: RunnableConfig):
    print("\n\ndata_collector" + "=" * 30)
    result = llm_tools.invoke([SystemMessage(content=query2tool)] + state["messages"], config)
    return {"messages": [result]}

tool_node = ToolNode([mongo_filter, mongo_aggregation, pinecone_search])

def final_chatbot(state: State, config: RunnableConfig):
    print("\n\nfinal_chatbot" + "=" * 30)
    result = llm_final_chatbot.invoke([SystemMessage(content=system)] + state["messages"], config)
    return {"messages": [result], "chat_history": [result]}

def ask_more(state: State, config: RunnableConfig):
    print("\n\nask_more" + "=" * 30)
    return {}

def request_query(state: State, config: RunnableConfig):
    print("\n\nrequest_query" + "=" * 30)
    return {}

def feedback(state: State, config: RunnableConfig):
    print("\n\nfeedback" + "=" * 30)
    return {}

