from src.Data_Ingestion import ingest_data
import chromadb
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import GPTVectorStoreIndex

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

config_path = "config.json"  

def process_and_store_index():
    # initialize client, setting path to save data
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("quickstart")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # create your index
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    documents = ingest_data(config_path)
    index = GPTVectorStoreIndex.from_documents(documents, storage_context=storage_context)
    return index

if __name__=="__main__":
    index  = process_and_store_index()

