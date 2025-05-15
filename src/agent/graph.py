from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

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
