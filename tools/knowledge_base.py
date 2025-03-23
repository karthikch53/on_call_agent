import json
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document


class KnowledgeBaseTool:
    CHROMA_DIR = "embeddings/knowledge"
    KB_FILE = "kb/past_requests.json"

    def create_kb_index(self):
        with open(self.KB_FILE) as f:
            data = json.load(f)
            print(data)
        docs = [Document(page_content=item["solution"], metadata={"issue": item["issue"]}) for item in data]
        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma.from_documents(docs, embedder, persist_directory=self.CHROMA_DIR)
        db.persist()

    def knowledge_base_search(self, query: str) -> [str]:
        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(persist_directory=self.CHROMA_DIR, embedding_function=embedder)
        results = db.similarity_search(query, k=5)
        contents = []
        for doc in results:
            contents.append(doc.page_content)
        return contents


if __name__ == '__main__':
    kb = KnowledgeBaseTool()
    kb.create_kb_index()
