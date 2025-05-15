from typing import TypedDict, Literal
from dataclasses import dataclass
from typing_extensions import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class Configuration(TypedDict):
    """Configurable parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """
    user_name: str

@dataclass
class State(TypedDict):
    """Input state for the agent.

    Defines the initial structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    """
    chat_history: Annotated[list[AnyMessage], add_messages]
    messages: Annotated[list[AnyMessage], add_messages]

    next_action: Annotated[Literal["history_filter", "context_collector", "request_query", "final_chatbot"], ..., "final_chatbot"]
    total_context_num: Annotated[int, ..., 0]
    output_context_num: Annotated[int, ..., 0]
    is_topic: Annotated[bool, ..., True]

class Output_Topic_Checker(TypedDict):
    result: Annotated[bool, None, "Is the query related to the topic, cheese?"]


