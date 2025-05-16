import json
from dotenv import load_dotenv
load_dotenv(".env")

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from src.agent.graph import graph_builder
from src.agent.prompt import hello
from src.model.agent import State


if __name__ == "__main__":

    checkpointer = InMemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)
    graph_code = graph.get_graph().draw_mermaid()

    print(f"Bot: {hello}")

    config = {
        "configurable": {
            "user_name": "Henrry Grant",
            "thread_id": "1"
        }
    }

    state : State = {
        "chat_history": [],
        "messages": [],
        "next_action": "request_query",
        "total_context_num": 0,
        "output_context_num": 0,
        "is_topic": True,
        "current_query": '',
        "interrupted": False
    }

    chat_index = 0
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["quit", "exit", "bye"]:
            print("Bot: Goodbye! Hope you enjoyed our cheesy chat!")
            break

        if not user_query.strip():
            continue

        if not state["interrupted"]:
            events = graph.stream(
                {
                    "messages": [HumanMessage(content=user_query)],
                } if chat_index else {
                    **state,
                    "messages": [HumanMessage(content=user_query)]
                },
                config,
                stream_mode="values",
            )
        else:
            events = graph.stream(Command(resume=user_query), config=config, stream_mode="values")

        for event in events:
            if "messages" in event:
                event["messages"][-1].pretty_print()

        state = graph.get_state(config).values
        if state["interrupted"]:
            print("Bot: " + state["current_query"])


