from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.types import interrupt
# from langchain_core.messages.utils import count_tokens_approximately
# from langmem.short_term import SummarizationNode

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
    result = llm_topic_checker.invoke([SystemMessage(content=isCheeseChat)] + state["chat_history"] + [state["messages"][-1]], config)
    return {"messages": [AIMessage(content=result["reason"])], "is_topic": result["result"]}

def general_chatbot(state: State, config: RunnableConfig):
    print("\n\ngeneral_chatbot" + "=" * 30)
    result = llm_general_chatbot.invoke([SystemMessage(content=general)] + state["chat_history"] + state["messages"][-2:], config)
    return {"chat_history": [state["messages"][-2], result]}

def history_filter(state: State, config: RunnableConfig):
    print("\n\nhistory_filter" + "=" * 30)
    result = llm_history_filter.invoke([SystemMessage(content=history)] + state["chat_history"], config)
    messages = [RemoveMessage(id=REMOVE_ALL_MESSAGES), state["messages"][-2], SystemMessage(content=f" In this conversation so far, {result.content}")]
    return {"messages": messages, "chat_history": [state["messages"][-2]]}

# history_filter = SummarizationNode(
#     token_counter=count_tokens_approximately,
#     model=llm_history_filter,
#     max_tokens=256,
#     max_tokens_before_summary=256,
#     max_summary_tokens=128,
#     input_messages_key="chat_history",
# )

def reasoner(state: State, config: RunnableConfig):
    print("\n\nreasoner" + "=" * 30)
    result = llm_reasoner.invoke([SystemMessage(content=reasoning)] + state["messages"], config)
    return {
        "messages": [AIMessage(content=result["reason"])],
        "next_action": result["choice"],
        "current_query": result["query"],
        "interrupted": result["choice"] == "request_query"
    }

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
    result = interrupt({
        "query": state["current_query"],
    })
    return {
        "messages": [HumanMessage(content=result)],
        "chat_history": [AIMessage(content=state["current_query"]), HumanMessage(content=result)]
    }

def feedback(state: State, config: RunnableConfig):
    print("\n\nfeedback" + "=" * 30)
    return {}

