from typing import TypedDict, Literal
from dataclasses import dataclass
from typing_extensions import Annotated
from pydantic import BaseModel, Field

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

    next_action: Literal["data_collector", "request_query", "final_chatbot"]
    total_context_num: int
    output_context_num: int
    is_topic: bool
    current_query: str
    interrupted: bool

class Output_Topic_Checker(TypedDict):
    result: Annotated[bool, None, "Is the query related to the topic, cheese?"]
    reason: Annotated[str, None, "The reason for why the query is related to the topic, or not."]

class Choice_Reasoner(TypedDict):
    choice: Literal["request_query", "data_collector", "final_chatbot"]
    reason: Annotated[str, None, "The reason for why you choose this action."]
    query: Annotated[str, None, "The question that you ask to tool or user for getting necessary data."]


