from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.config import ALLOWED_EXTENTIONS, MAX_FILE_SIZE, UPLOAD_DIR
import uuid
from app.service.document_parser import extract_text
from app.models import Contract
from app.database import contracts_collection

router=APIRouter(
    prefix="/contracts",
    tags=["contracts"]
)

@router.post("/upload")
async def upload_contracts(file: UploadFile = File(...)):

    # checking whether the extension of the file is correct
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENTIONS:
        raise HTTPException(status_code=400, detail="File type not allowed! Only upload .pdf and .txt files")

    # checking whether the file is in the size limit
    content = await file.read()
    size_md = len(content) / (1024*1024)
    if size_md > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Upload file of less than 10MB")

    # creating a folder to store the files as binary bytes with unique names 
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(file_path, "wb") as f:
        f.write(content)

    # actually extracting the text from the file
    parsed = extract_text(file_path)

    contract_data =Contract(
        filename=unique_name,
        original_name=file.filename,
        text_content=parsed["text"],
        page_count=int(parsed["page_count"]),
        word_count=int(parsed["word_count"])
    )

    docs = contract_data.model_dump()
    result = contracts_collection.insert_one(docs)
    contract_data.id = str(result.inserted_id)


    return {
        "message": "Contract uploaded successfully!",
        "contact": contract_data.model_dump(),
        "id": contract_data.id
    }

@router.get("/")
async def list_contracts():
    contracts=[]
    for doc in contracts_collection.find():
        contract = Contract(**doc)
        contract.id = str(doc["_id"])
        contracts.append(contract.model_dump())
    return {
        "contracts": contracts

    }

@router.get("/{id}")
async def get_contract(id: str):

    from bson import ObjectId
    doc = contracts_collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Contract not found")

    contract = Contract(**doc)
    contract.id = str(doc["_id"])
    return {
        "contract": contract.model_dump()
    }