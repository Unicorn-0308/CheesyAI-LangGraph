import json
import uuid
import re
from dotenv import load_dotenv
import streamlit as st
try:
    load_dotenv('.env')
except:
    pass

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from src.model.agent import State
from src.agent.graph import graph_builder
from src.agent.prompt import hello


def set_page_config():
    st.set_page_config(
        page_title="CheesyChat",
        page_icon="🧀",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://shop.kimelo.com/department/cheese/3365',
            'Report a bug': None,
            'About': "## 🧀 CheesyChat \n Your friendly AI assistant for all things cheese!"
        }
    )


def set_page_style():
    st.markdown(
        f"""
        <style>
        {open("assets/style.css").read()}
        </style>
    """,
        unsafe_allow_html=True,
    )
    pass


def initialize_session_state():
    """Initialize session state variables."""
    if "graph" not in st.session_state:
        checkpointer = InMemorySaver()
        st.session_state.graph = graph_builder.compile(checkpointer=checkpointer)

    # if "messages" not in st.session_state:
    #     st.session_state.messages = []

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if "active_prompt" not in st.session_state:
        st.session_state.active_prompt = False

    if "thinking" not in st.session_state:
        st.session_state.thinking = False

    if "reasoning" not in st.session_state:
        st.session_state.reasoning = {}

    if "config" not in st.session_state:
        st.session_state.config = {
            "configurable": {
                "user_name": "User",
                "thread_id": st.session_state.thread_id,
            }
        }


def setup_sidebar():
    """Configure the sidebar with agent information and controls."""
    with st.sidebar:
        st.markdown(
            """
            <div class="agent-profile">
                <div class="profile-header">
                    <div class="avatar">🤖</div>
                    <h1>Cheesy Chatbot</h1>
                </div>
                <div class="feature-list">
                    <div class="feature-item">
                        <span class="icon">🛒</span>
                        <span>Browse available products</span>
                    </div>
                </div>
                <div class="status-card">
                    <div class="status-indicator"></div>
                    <span>Ready to Assist</span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        if st.button("🔄 Start New Chat", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        if st.button("🔍 Visualize Workflow", use_container_width=True):
            st.image("assets/graph.png")

        st.markdown(
            """
            <div class="sidebar-footer">
                <div class="powered-by">
                    Enhanced by AI • Crafted for You
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

def process_reason(message, node):
    if isinstance(message, ToolMessage):
        try:
            result = re.sub(r"ObjectId\('([^']*)'\)", r"'\1'", message.content)
            result = result.replace("\"", "\\")
            result = result.replace("\'", "\"")
            result = result.replace("\\", "\'")
            result = result.replace("\n", "")
            result = result.replace("True", "true")
            result = result.replace("False", "false")
            result = json.loads(result)
        except Exception as e:
            result = []
        data = {
            "Name": message.name,
            "Result": result,
            "Tool_ID": message.tool_call_id
        }
        data = json.dumps(data, indent=2)
        return {
            "type": "code",
            "node": node,
            "data": data,
        }
    else:
        if hasattr(message, "tool_calls") and message.tool_calls:
            data = [{
                "Name": tool["name"],
                "Args": tool["args"],
                "Tool_ID": tool["id"],
            } for tool in message.tool_calls]
            data = json.dumps(data, indent=2)
            return {
                "type": "code",
                "node": node,
                "data": data,
            }
        else:
            return {
                "type": "text",
                "node": node,
                "data": message.content,
            }

def display_reason(data, step):
    if data["node"] == "reasoner":
        st.info(f"# Step  {step}")
        st.markdown("### Thought")
    elif data["node"] == "data_collector":
        st.markdown("### Action")
    elif data["node"] == "tool_node":
        st.markdown("### Data")
    else:
        return

    if data['type'] == 'code':
        st.code(data['data'], language='json')
    else:
        st.markdown(data['data'])

def display_chat_history():
    """Display the chat history."""
    st.markdown(
        f"""
                <div style='text-align: center; padding: 30px;'>
                    <h1>👋 Welcome!</h1>
                </div>
                """,
        unsafe_allow_html=True,
    )
    if 'state' not in st.session_state:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 30px;'>
                <p>🧀{hello}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for message in st.session_state.state["chat_history"]:
            if isinstance(message, HumanMessage):
                with st.chat_message(name="user"):
                    st.markdown(message.content)
            else:
                with st.chat_message(name="assistant", avatar="🤖"):
                    if message.id not in [m.id for m in st.session_state.state["chat_history"][:2]]:
                        with st.expander("Reasoning", expanded=False):
                            index = 1
                            for reason in st.session_state.reasoning[message.id]:
                                display_reason(reason, index)
                                if reason["node"] == "reasoner":
                                    index += 1
                    st.markdown(message.content)


def main():
    set_page_config()
    set_page_style()
    initialize_session_state()
    setup_sidebar()

    display_chat_history()

    # if st.session_state.pending_approval:
    #     handle_tool_approval(*st.session_state.pending_approval)

    if prompt := st.chat_input("Your Message: ", disabled=st.session_state.thinking):
        st.session_state.active_prompt = prompt
        st.session_state.thinking = True
        st.rerun()

    if st.session_state.thinking and st.session_state.active_prompt:
        human_message = HumanMessage(content=st.session_state.active_prompt)
        with st.chat_message("user"):
            st.markdown(st.session_state.active_prompt)

        try:
            with st.spinner("Thinking..."):
                st.session_state.thinking = True

                if "state" not in st.session_state or not st.session_state.state["interrupted"]:
                    events = st.session_state.graph.stream(
                        {
                            "chat_history": [human_message],
                            "messages": [human_message],
                        } if "state" in st.session_state else {
                            "chat_history": [AIMessage(content=f"🧀{hello}"), human_message],
                            "messages": [human_message],
                            "next_action": "request_query",
                            "total_context_num": 0,
                            "output_context_num": 0,
                            "is_topic": True,
                            "current": '',
                            "interrupted": False
                        },
                        st.session_state.config,
                        stream_mode="values",
                    )
                else:
                    events = st.session_state.graph.stream(Command(resume=st.session_state.active_prompt), config=st.session_state.config, stream_mode="values")

                reasons = []
                with st.chat_message("assistant", avatar="🤖"):
                    with st.expander("Reasoning...", expanded=False):
                        index = 1
                        for event in events:
                            if "messages" in event:
                                reason = event["messages"][-1]
                                if event["current"] in ["final_chatbot", "ask_more", "request_query", "general_chatbot", "feedback"] or isinstance(reason, HumanMessage):
                                    # reason.pretty_print()
                                    continue
                                elif isinstance(reason, ToolMessage):
                                    i = 1
                                    while isinstance(event["messages"][-i], ToolMessage):
                                        i += 1
                                    for reason in event["messages"][-i + 1:]:
                                        # reason.pretty_print()
                                        data = process_reason(reason, "tool_node")
                                        reasons.append(data)
                                        display_reason(data, index)
                                else:
                                    # reason.pretty_print()
                                    data = process_reason(reason, event["current"])
                                    reasons.append(data)
                                    display_reason(data, index)
                                    if data["node"] == "reasoner":
                                        index += 1

                st.session_state.state = st.session_state.graph.get_state(st.session_state.config).values
                st.session_state.reasoning[st.session_state.state["chat_history"][-1].id] = reasons

        except Exception as e:
            st.error(f"Error processing message: {str(e)}")
            print(str(e))

        finally:
            st.session_state.thinking = False
            st.session_state.active_prompt = None
            st.rerun()


if __name__ == "__main__":
    main()
