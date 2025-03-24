import json
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import os


class KnowledgeBaseTool:
    CHROMA_DIR = "/Users/karthick.rameshkumar/Documents/codebase/on_call_agent/embeddings/knowledge"
    KB_FILE = "../kb/past_requests.json"

    def create_kb_index(self):
        with open(self.KB_FILE) as f:
            data = json.load(f)
            print(data)
        docs = [Document(page_content=item["solution"], metadata={"issue": item["issue"]}) for item in data]
        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        os.makedirs(self.CHROMA_DIR, exist_ok=True)
        Chroma.from_documents(docs, embedder, persist_directory=self.CHROMA_DIR)

    def knowledge_base_search(self, query: str) -> [str]:
        print(f"searching for {query}")
        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(persist_directory=self.CHROMA_DIR, embedding_function=embedder)
        results = db.similarity_search(query, k=5)
        _contents = []
        for doc in results:
            _contents.append(doc.page_content)
        return _contents


if __name__ == '__main__':
    kb = KnowledgeBaseTool()
    kb.create_kb_index()
    contents = kb.knowledge_base_search('I never received the verification email')
    print(contents)
