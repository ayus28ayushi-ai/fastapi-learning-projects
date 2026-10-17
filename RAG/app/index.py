from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore


load_dotenv()

pdf_path = Path(__file__).parent / "data" / "aiayn.pdf"


# loading the pdf 
loader = PyMuPDFLoader(str(pdf_path))
docs = loader.load()

#splitting the documents into chunks 
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks = text_splitter.split_documents(documents=docs)

# embedding the chunks into OpenAI Embeddings
embedding_model = HuggingFaceEmbeddings(
    model="all-MiniLM-L6-v2"
)

# creating a qdrant vector store
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="sample_collection",
    url="http://localhost:6333",
    force_recreate=True
)

print("Vector store created and documents embedded successfully!")