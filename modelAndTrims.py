import os
import openai
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import docx
import json

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API configurations
openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")


class DocumentParser:
    def documents(self):
        doc_file_path = "BMW.docx"
        doc = docx.Document(doc_file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        try:
            # Attempt to parse the extracted text as JSON
            json_data = json.loads(text)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None


class DataPreProcess:
    def preprocess(self, json):
        s = set()
        for i in json:
            s.add(i["content"])
        print(len(s))
        return s


class extractTrimsFromText:
    def extract(self):
        doc_parse = DocumentParser()
        jsonList = doc_parse.documents()
        if jsonList == None:
            print("No json data to read")
            return
        else:
            data_preprocess = DataPreProcess()
            json = data_preprocess.preprocess(jsonList)
            prompt = f"identify the models with their trims from the following html {json} and generate a table with no duplicate entries. For example if the object is given as 'F 850 Adventure', then the model name is 'F' and trim is '850 Adventure'. Another example if object is 'R NineT Pure', then model is 'R' and trim is 'NineT Pure'"
            chat = ChatOpenAI(temperature=0.9, engine="GPT3-5")
            response = chat.predict(prompt)
            return response


def main():
    trims = extractTrimsFromText()
    output = trims.extract()
    print(output)


if __name__ == "__main__":
    main()
