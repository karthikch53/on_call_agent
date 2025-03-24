from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


class RunbookSearchTool:
    CHROMA_DIR = "/Users/karthick.rameshkumar/Documents/codebase/on_call_agent/embeddings/runbooks"
    RUNBOOKS_DIR = "../runbooks"

    def create_runbook_index(self):
        loader = DirectoryLoader(self.RUNBOOKS_DIR, glob="**/*.md")
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)
        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        os.makedirs(self.CHROMA_DIR, exist_ok=True)
        Chroma.from_documents(chunks, embedder, persist_directory=self.CHROMA_DIR)

    def search_runbooks(self, query: str) -> [str]:
        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(persist_directory=self.CHROMA_DIR, embedding_function=embedder)
        results = db.similarity_search(query, k=5)
        contents = []
        for doc in results:
            contents.append(doc.page_content)
        return contents


if __name__ == '__main__':
    rb = RunbookSearchTool()
    rb.create_runbook_index()
