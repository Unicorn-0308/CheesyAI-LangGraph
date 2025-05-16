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
    filtered_history: list[AnyMessage]

    next_action: Annotated[Literal["history_filter", "data_collector", "request_query", "final_chatbot"], ..., "final_chatbot"]
    total_context_num: Annotated[int, ..., 0]
    output_context_num: Annotated[int, ..., 0]
    is_topic: Annotated[bool, ..., True]

class Output_Topic_Checker(TypedDict):
    result: Annotated[bool, None, "Is the query related to the topic, cheese?"]
    reason: Annotated[str, None, "The reason for why the query is related to the topic, or not."]

class Choice_Reasoner(TypedDict):
    choice: Literal["history_filter", "data_collector", "final_chatbot"]
    reason: Annotated[str, None, "The reason for why you choose this action."]

class History_Filter(BaseModel):
    chat: Annotated[list[AnyMessage], None, "Messages that are necessary to answer the user's query."]

    class Config:
        arbitrary_types_allowed = True


