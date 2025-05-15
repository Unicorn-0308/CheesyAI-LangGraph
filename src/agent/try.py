import os
from langchain.chat_models import init_chat_model


llm = init_chat_model("openai:gpt-4.1")

from typing import Annotated

from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

graph_builder = StateGraph(State)

tool = TavilySearch(max_results=2, tavily_api_key="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")
tools = [tool, multiply]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool, multiply])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

for event in graph.stream({"messages": ["What is 46 x 8 and 6 x 7?"]}, stream_mode="values"):
    if "messages" in event:
        event["messages"][-1].pretty_print()
