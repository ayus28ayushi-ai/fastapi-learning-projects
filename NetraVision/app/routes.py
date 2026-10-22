import uuid
from app.services.vision import analyze_image
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.image import validate_image, resize_image_if_needed, save_image

router = APIRouter()


async def process_single_file(file: UploadFile):
    content = await file.read()
    # validating the file type and size
    validation = validate_image(content, file.content_type)
    if not validation["is_valid"]:
        raise HTTPException(status_code=400, detail=validation["message"])

    # resizing the image if needed and saving it
    processed = resize_image_if_needed(content)
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    save_image(processed, "uploads", unique_name)
    result = await analyze_image(processed, file.content_type)

    print(f"Analysis result for {file.filename}: {result}")
    return result

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid File type")

    result = await process_single_file(file)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "Image received and processed for disease detection.",
        "result": result
    }
