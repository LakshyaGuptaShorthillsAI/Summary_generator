import streamlit as st
from dotenv import load_dotenv
import openai
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI

class PDFProcessor:
    def __init__(self, pdf_path):
        print(self)
        self.pdf_path = pdf_path

    def get_pdf_text(self):
        text = ""
        pdf_reader = PdfReader(self.pdf_path)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

class TextChunker:
    def __init__(self, separator="\n", chunk_size=1000, chunk_overlap=200):
        self.separator = separator
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text):
        text_splitter = CharacterTextSplitter(
            separator=self.separator,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks

class VectorStoreCreator:
    def __init__(self, model_name):
        self.model_name = model_name

    def create_vectorstore(self, text_chunks):
        embeddings = HuggingFaceInstructEmbeddings(model_name=self.model_name)
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore

class LoanSummaryGenerator:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def generate_summary(self, query):
        response = self.vectorstore.similarity_search(query)
        para = response[0].page_content
        llm = ChatOpenAI(engine="GPT3-5")
        q = "Write a short summary from the following {text}"
        llm_query = q.format(text = para)
        summary = llm.predict(llm_query)
        return summary

def main():
    load_dotenv()
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    
    pdf_processor = PDFProcessor("LOAN AGREEMENT .pdf")
    raw_text = pdf_processor.get_pdf_text()
    
    text_chunker = TextChunker()
    text_chunks = text_chunker.split_text(raw_text)

    vectorstore_creator = VectorStoreCreator(model_name="hkunlp/instructor-xl")
    vectorstore = vectorstore_creator.create_vectorstore(text_chunks)
    
    summary_generator = LoanSummaryGenerator(vectorstore)
    query = "Write a summary of the loan document"
    summary = summary_generator.generate_summary(query)
    print(summary)
    
    

if __name__ == '__main__':
    main()

