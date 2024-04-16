import chromadb
from llama_index.core import GPTVectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import google.generativeai as palm
from llama_index.llms.palm import PaLM
import os
from dotenv import load_dotenv
load_dotenv()

KEY = os.getenv("GOOGLE_API_KEY")
palm.configure(api_key=KEY)

from llama_index.core import Settings
Settings.llm = PaLM(model_name="models/text-bison-001", api_key=KEY, temperature=0.1)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def load_index():
    # initialize client
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("quickstart")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # load your index from stored vectors
    index = GPTVectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    return index
