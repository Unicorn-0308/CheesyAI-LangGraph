import os

from langchain.chat_models import init_chat_model

from src.model.agent import Output_Topic_Checker

llm_topic_checker = init_chat_model(os.environ["MODEL_TOPIC_CHECKER"]).with_structured_output(Output_Topic_Checker)


