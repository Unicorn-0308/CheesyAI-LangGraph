from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from langgraph.graph import StateGraph

from src.model.agent import State, Configuration
from src.agent.node import (
    topic_checker,
    general_chatbot,
    reasoner,
    history_filter,
    context_collector,
    final_chatbot,
    ask_more,
    request_query
)

graph_builder = StateGraph(State, Configuration)

# Add Nodes
graph_builder.add_node("topic_checker", topic_checker)
graph_builder.add_node("general_chatbot", general_chatbot)
graph_builder.add_node("reasoner", reasoner)
graph_builder.add_node("history_filter", history_filter)
graph_builder.add_node("context_collector", context_collector)
graph_builder.add_node("final_chatbot", final_chatbot)
graph_builder.add_node("ask_more", ask_more)
graph_builder.add_node("request_query", request_query)

# Add Edges

