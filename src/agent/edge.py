from typing import Literal

from src.model.agent import State

def conditional_topic_checker(state: State) -> Literal["general_chatbot", "history_filter"]:
    return "history_filter" if state["is_topic"] else "general_chatbot"

def conditional_reasoner(state: State) -> Literal["data_collector", "request_query", "final_chatbot"]:
    return state["next_action"]

def conditional_final_chatbot(state: State) -> Literal["ask_more", "feedback"]:
    # return "ask_more" if state["output_context_num"] < state["total_context_num"] else "feedback"
    return "feedback"
