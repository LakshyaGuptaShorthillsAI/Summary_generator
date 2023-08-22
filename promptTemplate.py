import os
import openai
from langchain import OpenAI
from langchain import PromptTemplate
import dotenv
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

llm = OpenAI(temperature=0.9, engine="GPT3-5")
template = "Write something about {subject}"
prompt = PromptTemplate(
    input_variables=["subject"],
    template=template
)
msg=prompt.format(subject="skydiving")
print(llm(msg))

