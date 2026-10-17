from fastapi import APIRouter, HTTPException
from app.config import GEMINI_API_KEY
from app.database import contracts_collection
from app.service.analyse_contract import analyse_contract
from app.database import analysis_collection

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"]
)

@router.post("/analyse/{contract_id}")
async def analyse_contract_by_id(contract_id: str):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI API key not configured")

    from bson import ObjectId
    contract = contracts_collection.find_one({"_id": ObjectId(contract_id)})

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    if not contract.get("text_content"):
        raise HTTPException(status_code=400, detail="Contract has no text to analyze")

    contracts_collection.update_one({
        "_id": ObjectId(contract_id)},
        {"$set" : {"analysis_status": "in_progress"}})

    result = await analyse_contract(contract_id, contract["text_content"])
    doc = result.model_dump()
    insert_result = analysis_collection.insert_one(doc)
    result.id = str(insert_result.inserted_id)

    contracts_collection.update_one({
            "_id": ObjectId(contract_id)},
            {"$set" : {"analysis_status": "completed"}})

    return {
        "message": "Contract anlyzed successfully",
        "analysis": result.model_dump(),
        "id": result.id
    }