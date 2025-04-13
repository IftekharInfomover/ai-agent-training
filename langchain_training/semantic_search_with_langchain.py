from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_core.vectorstores import InMemoryVectorStore
import asyncio


load_dotenv()


class SemanticSearch:

    def __init__(self, _api_key, file_path = "../nke-10k-2023.pdf",):
        self.api_key = _api_key
        self.file_path = file_path
        self.docs = self.document_loader()
        self.all_splits = self.splitter()
        self.embeddings = MistralAIEmbeddings(model="mistral-embed")
        self.vector_store = self.create_vector_store()


    def document_loader(self):
        loader = PyPDFLoader(self.file_path)
        docs = loader.load()
        return docs


    def splitter(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        all_splits = text_splitter.split_documents(self.docs)
        return all_splits


    def create_vector_store(self):
        vector_store = InMemoryVectorStore(self.embeddings)
        vector_store.add_documents(documents=self.all_splits)
        return  vector_store

    def similarity_search(self):
        results = self.vector_store.similarity_search(
            "How many distribution centers does Nike have in the US?"
        )
        return results[0]

    async def perform_search(self):
        results = await self.vector_store.asimilarity_search("When was Nike incorporated?")
        return results[0]


if __name__ == "__main__":
    api_key = os.getenv('MISTRAL_API_KEY')
    if api_key is None:
        print('Please set the environment variable Mistral API key')
        exit(1)
    search = SemanticSearch(api_key)
    print(search.similarity_search())

    # async_result = asyncio.run(
    #     search.async_search("When was Nike incorporated?")
    # )
    # print(async_result if async_result else "No async results found")
