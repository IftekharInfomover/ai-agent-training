from importlib.metadata import metadata
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv
import getpass
import os
from langchain_core.vectorstores import InMemoryVectorStore
import asyncio


load_dotenv()

file_path = "../nke-10k-2023.pdf"   ### In this case file is kept in the parent folder of project
loader = PyPDFLoader(file_path)

docs = loader.load()

print(len(docs))
print(f"{docs[0].page_content[:200]}\n")
print(docs[0].metadata)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

print(len(all_splits))

# if not os.environ.get("MISTRALAI_API_KEY"):
#     os.environ["MISTRALAI_API_KEY"] = getpass.getpass("Enter API key for MistralAI: ")

if not os.environ.get("MISTRAL_API_KEY"):
    os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")

api_key = os.getenv('MISTRAL_API_KEY')

embeddings = MistralAIEmbeddings(model="mistral-embed")

vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)

assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])

vector_store = InMemoryVectorStore(embeddings)

ids = vector_store.add_documents(documents=all_splits)

results = vector_store.similarity_search(
    "How many distribution centers does Nike have in the US?"
)
print(results[0])

async def perform_search():
    results = await vector_store.asimilarity_search("When was Nike incorporated?")
    print(results[0])

# Run the asynchronous function
asyncio.run(perform_search())






# class SemanticSearch:
#
#     def __init__(self, _api_key, file_path = "../nke-10k-2023.pdf",):
#         self.api_key = _api_key
#         self.file_path = file_path
#         self.document_loader()
#         self.splitter()
#         self.embeddings_generator()
#
#
#     def document_loader(self):
#         file_path = self.file_path
#         loader = PyPDFLoader(file_path)
#         docs = loader.load()
#
#         len_docs = len(docs)
#         page_content = f"{docs[0].page_content[:200]}\n"
#         metadata = docs[0].metadata
#
#         return docs
#
#     def splitter(self):
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000, chunk_overlap=200, add_start_index=True
#         )
#         all_splits = text_splitter.split_documents(self.document_loader())
#         return all_splits
#
#     def embeddings_generator(self):
#         embeddings = MistralAIEmbeddings(model="mistral-embed")
#         vector_1 = embeddings.embed_query(self.splitter()[0].page_content)
#         vector_2 = embeddings.embed_query(self.splitter()[1].page_content)
#         assert len(vector_1) == len(vector_2)
#
#         return embeddings
#
#     def vector_store(self):
#         vector_store = InMemoryVectorStore(self.embeddings_generator())
#         ids = vector_store.add_documents(documents=self.splitter())
#         return  vector_store
#
#     def similarity_search(self):
#         results = self.vector_store().similarity_search(
#             "How many distribution centers does Nike have in the US?"
#         )
#         return results[0]
#
#     def async_search(self):
#         async def perform_search():
#             results = await self.vector_store().asimilarity_search("When was Nike incorporated?")
#             print(results[0])
#         return asyncio.run(perform_search())
#
#
# if __name__ == "__main__":
#     api_key = os.getenv('MISTRAL_API_KEY')
#     if api_key is None:
#         print('Please set the environment variable Mistral API key')
#         exit(1)
#     search = SemanticSearch(api_key)
#     print(search.similarity_search())





