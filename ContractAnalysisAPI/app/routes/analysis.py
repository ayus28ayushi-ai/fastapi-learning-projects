from fastapi import APIRouter, HTTPException
from app.config import GEMINI_API_KEY
from app.database import contracts_collection
from app.service.analyse_contract import analyse_contract
from app.database import analysis_collection
from app.models import AnalysisResult

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

    result =  await analyse_contract(contract_id, contract["text_content"])
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

@router.get("/{analysis_id}")
async def get_analysis_by_id(analysis_id: str):
    from bson import ObjectId
    analysis_to_find =   analysis_collection.find_one({"_id": ObjectId(analysis_id)})
    if not analysis_to_find:
        raise HTTPException(status_code=404, detail="Analysis not found for this contract")

    analysis_to_find["id"] = str(analysis_to_find['_id'])
    del analysis_to_find["_id"]
    return AnalysisResult(**analysis_to_find)

@router.get("/contract/{contract_id}")
async def get_analysis_for_contract(contract_id: str):
    list_of_records = list(analysis_collection.find({"contract_id": contract_id}))

    if not list_of_records:
        raise HTTPException(status_code=404, detail="No analysis found for this contract")
    for record in list_of_records:
        record["id"] = str(record['_id'])
        del record["_id"]
    return list_of_records

@router.get("/")
def list_all_analysis():
    analysis = []
    for doc in analysis_collection.find({}):
        doc['id'] = str(doc['_id'])
        del doc['_id']
        analysis.append(doc)
    return {"analysis": analysis}