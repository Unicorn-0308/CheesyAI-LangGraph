import json
from dotenv import load_dotenv
load_dotenv(".env")

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from src.agent.graph import graph_builder
from src.agent.prompt import hello


if __name__ == "__main__":

    checkpointer = InMemorySaver()
    graph = graph_builder.compile(checkpointer=checkpointer)

    print(f"Bot: {hello}")

    config = {
        "configurable": {
            "user_name": "Henrry Grant",
            "thread_id": "1"
        }
    }

    while True:
        user_query = input("You: ")
        if user_query.lower() in ["quit", "exit", "bye"]:
            print("Bot: Goodbye! Hope you enjoyed our cheesy chat!")
            break

        if not user_query.strip():
            continue

        state = graph.get_state(config)

        events = graph.stream(
            {
                "messages": [HumanMessage(content=user_query)],
            },
            config,
            stream_mode="values",
        )
        for event in events:
            if "messages" in event:
                event["messages"][-1].pretty_print()
