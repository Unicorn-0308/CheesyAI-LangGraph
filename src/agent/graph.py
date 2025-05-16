from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from langgraph.graph import StateGraph, END

from src.model.agent import State, Configuration
from src.agent.node import (
    topic_checker,
    general_chatbot,
    reasoner,
    history_filter,
    data_collector,
    tool_node,
    final_chatbot,
    ask_more,
    request_query,
    feedback
)
from src.agent.edge import (
    conditional_topic_checker,
    conditional_reasoner,
    conditional_final_chatbot
)

graph_builder = StateGraph(State, Configuration)

# Add Nodes
graph_builder.add_node("topic_checker", topic_checker)
graph_builder.add_node("general_chatbot", general_chatbot)
graph_builder.add_node("reasoner", reasoner)
graph_builder.add_node("history_filter", history_filter)
graph_builder.add_node("data_collector", data_collector)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("final_chatbot", final_chatbot)
graph_builder.add_node("ask_more", ask_more)
graph_builder.add_node("request_query", request_query)
graph_builder.add_node("feedback", feedback)

# Add Edges
graph_builder.set_entry_point("topic_checker")
graph_builder.add_conditional_edges("topic_checker", conditional_topic_checker)
graph_builder.add_edge("general_chatbot", "feedback")

graph_builder.add_edge("history_filter", "reasoner")
graph_builder.add_conditional_edges("reasoner", conditional_reasoner)
graph_builder.add_edge("data_collector", "tools")
graph_builder.add_edge("tools", "reasoner")
graph_builder.add_edge("request_query", "reasoner")
graph_builder.add_conditional_edges("final_chatbot", conditional_final_chatbot)
graph_builder.add_edge("ask_more", "final_chatbot")

graph_builder.add_edge("feedback", END)


if __name__ == "__main__":
    graph = graph_builder.compile()

    events = graph.stream(
        {
            "messages": [{"role": "user", "content": "Hello!"}],
            "is_topic": True,
            "next_action": "final_chatbot",
            "total_context_num": 0,
            "output_context_num": 0,
        },
        {
            "configurable": {
                "user_name": "Henrry Grant",
                "thread_id": "1"
            }
        },
        stream_mode="values",
    )
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()

