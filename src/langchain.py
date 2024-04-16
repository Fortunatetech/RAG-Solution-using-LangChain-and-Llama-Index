# import pprint
# import google.generativeai as palm
# from llama_index.llms.palm import PaLM

# palm_api_key = "AIzaSyDi6pgyhOai6zPHFuDoklgem9DiW7CEhFQ"
# palm.configure(api_key=palm_api_key)


# from llama_index.core import Settings
# Settings.llm = PaLM(model_name="models/text-bison-001", api_key=palm_api_key, temperature=0.1)


# index = VectorStoreIndex.from_documents(
#     documents, embed_model=embed_model
# )

# query_engine = index.as_query_engine(llm=llm)