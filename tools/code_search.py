from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os


class CodeSearchTool:
    CHROMA_DIR = "/Users/karthick.rameshkumar/Documents/codebase/on_call_agent/embeddings/code"
    CODE_PATH = "/Users/karthick.rameshkumar/Documents/codebase/simple-notes-app"
    RUNBOOKS_DIR = "runbooks"

    def index_code(self):
        loader = DirectoryLoader(self.CODE_PATH, glob="**/*.*",
                                 loader_cls=TextLoader, load_hidden=False,
                                 exclude=["*.war", "*.class", "*.war.*", "*.jar", "*.lst"]
                                 )
        docs = loader.load()
        print(len(docs))
        for doc in docs:
            print(doc.metadata['source'])
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)
        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        os.makedirs(self.CHROMA_DIR, exist_ok=True)
        Chroma.from_documents(chunks, embedder, persist_directory=self.CHROMA_DIR)

    def search_code(self, query: str) -> [str]:
        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = Chroma(persist_directory=self.CHROMA_DIR, embedding_function=embedder)
        results = db.similarity_search(query, k=5)
        content = []
        for doc in results:
            _metadata = doc.metadata
            _source = _metadata['source']
            _page_content = doc.page_content
            content.append(_page_content)
        return content


if __name__ == '__main__':
    cs = CodeSearchTool()
    #cs.index_code()
    contents = cs.search_code("where is mongodb collection defined?")
    for c in contents:
        print('---')
        print(c)
