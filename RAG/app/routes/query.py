from fastapi import APIRouter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import ChatOllama
from pydantic import BaseModel

router=APIRouter(
    prefix="/query",
    tags=["query"]
)

class QueryRequest(BaseModel):
    question: str

embedding_model = HuggingFaceEmbeddings(
    model="all-MiniLM-L6-v2"
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="sample_collection",
    url="http://localhost:6333"
)

llm = ChatOllama(model="llama3.2")


@router.post("/")
async def query(request: QueryRequest):
    answer = vector_db.similarity_search(query=request.question, k=3)

    context="\n\n".join(
        [
            f"[Page {result.metadata.get('page', 'unknown')}] {result.page_content}"
            for result in answer   
        ]
    )

    SYSTEM_PROMPT=f"""You are a helpful assistant that answers questions based on the provided context.
    If the context does not contain the answer, respond with "I don't know,"
    
    Context: {context}
    """

    message = [
        ("system", SYSTEM_PROMPT),
        ("human", request.question)
    ]

    llm_response= llm.invoke(message)

    return {
         "question": request.question, 
         "answer": llm_response.content,
         "source_chunks": answer}