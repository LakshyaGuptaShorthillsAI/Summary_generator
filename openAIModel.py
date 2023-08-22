from langchain.chat_models import ChatOpenAI
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

llm = ChatOpenAI(engine="GPT3-5")
try:
    response = llm.predict("What day comes after thursday")
    print(response)
except Exception as e:
    print(e)  
        