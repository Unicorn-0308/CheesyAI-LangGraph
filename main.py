import json
from dotenv import load_dotenv
load_dotenv(".env")

from langchain_core.messages import HumanMessage

from src.agent.graph import graph_builder


if __name__ == "__main__":
    graph = graph_builder.compile()

    events = graph.stream(
        {
            "messages": [HumanMessage(content="Hello! What is the most expensive?")],
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
