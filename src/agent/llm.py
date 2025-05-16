import os

from langchain.chat_models import init_chat_model

from src.model.agent import Output_Topic_Checker, Choice_Reasoner
from src.agent.tool import mongo_filter, mongo_aggregation, pinecone_search

llm_topic_checker = init_chat_model(os.environ["MODEL_TOPIC_CHECKER"]).with_structured_output(Output_Topic_Checker)
llm_general_chatbot = init_chat_model(os.environ["MODEL_GENERAL_CHATBOT"])
llm_reasoner = init_chat_model(os.environ["MODEL_REASONER"]).with_structured_output(Choice_Reasoner)
llm_tools = init_chat_model(os.environ["MODEL_TOOLS"]).bind_tools([mongo_filter, mongo_aggregation, pinecone_search])
