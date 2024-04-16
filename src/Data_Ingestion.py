import json
import os
import pandas as pd

import requests
from bs4 import BeautifulSoup
import docx2txt
import PyPDF2

import mysql.connector

from llama_index.core import GPTVectorStoreIndex
from llama_index.core.readers.base import BaseReader
from llama_index.core import Document


class PDFReader(BaseReader):
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        with open(self.file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)

            all_text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                all_text += page_text

        metadata = {"source": "pdf", "filename": os.path.basename(self.file_path)}
        document = Document(text=all_text, metadata=metadata)
        return [document]

class DOCXReader(BaseReader):
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        text = docx2txt.process(self.file_path) 

        metadata = {"source": "docx", "filename": os.path.basename(self.file_path)}
        document = Document(text=text, metadata=metadata)
        return [document] 
    
class TXTReader(BaseReader):
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        with open(self.file_path, "r") as f:
            text = f.read()
        metadata = {"source": "txt", "filename": os.path.basename(self.file_path)} 
        document = Document(text=text, metadata=metadata)
        return [document] 

class JSONReader(BaseReader):
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        with open(self.file_path, "r") as f:
            data = json.load(f)
        return [
            Document(text=item["content"], metadata={"source": "json", "item": item.get("metadata")}) 
            for item in data
        ] 

class CSVReader(BaseReader):
    def __init__(self, file_path, text_column, metadata_columns=None):
        self.file_path = file_path
        self.text_column = text_column
        self.metadata_columns = metadata_columns

    def load_data(self):
        df = pd.read_csv(self.file_path)
        return [
            {
                "text": row[self.text_column],
                "metadata": {col: row[col] for col in self.metadata_columns}
                if self.metadata_columns
                else {},
            }
            for _, row in df.iterrows()
        ]

class WebScraper(BaseReader):
    def __init__(self, url, text_selector):
        self.url = url
        self.text_selector = text_selector

    def load_data(self):
        response = requests.get(self.url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, "html.parser")
        elements = soup.select(self.text_selector)
        return [Document(text=element.text.strip(), metadata={"source": self.url})  
                for element in elements] 

class DatabaseReader(BaseReader):
    def __init__(self, connection_params, query, text_column, metadata_columns=None):
        self.connection_params = connection_params
        self.query = query
        self.text_column = text_column
        self.metadata_columns = metadata_columns

    def load_data(self):
        with mysql.connector.connect(**self.connection_params) as conn:
            with conn.cursor() as cur:
                cur.execute(self.query)
                results = cur.fetchall()

        return [
                    Document(
                        text=row[self.text_column],
                        metadata={col: row[col] for col in self.metadata_columns} 
                        if self.metadata_columns 
                        else {}  
                    )
                    for row in results
                ] 


def ingest_data(config_path): 
    with open(config_path, "r") as f:
        config = json.load(f)
    data_sources = config["data_sources"]

    index_documents = [] 

    for source in data_sources:
        reader_type = source["type"]  
        if reader_type == "json":
            reader = JSONReader(source["path"])
        elif reader_type == "csv":
            reader = CSVReader(source["path"], source["text_column"], source.get("metadata_columns"))
        elif reader_type == "pdf":
            reader = PDFReader(source["path"])
        elif reader_type == "docx":
            reader = DOCXReader(source["path"])
        elif reader_type == "txt":
            reader = TXTReader(source["path"])
        elif reader_type == "database":
            reader = DatabaseReader(
                connection_params=source["connection_params"],
                query=source["query"],
                text_column=source["text_column"], 
                metadata_columns=source.get("metadata_columns"),
            )
        elif reader_type == "webscraper":
            reader = WebScraper(source["url"], source["text_selector"])
        else:
            raise ValueError(f"Unsupported data source type: {reader_type}") 

        documents = reader.load_data()
        index_documents.extend(documents)

    return index_documents

   