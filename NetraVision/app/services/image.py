from PIL import Image
import io, os

ALLOWED_IAMGE_TYPES = ["image/jpeg", "image/png", "image/gif"]
MAX_IMAGE_DIMENSION = 2048

# IMAGE VALILDATION TO CHECK WHETHER THE IMAGE IS OOF PROPER TYPE OR NOT
def validate_image(content:bytes, content_type: str) -> dict:
    if not content_type.startswith("image/"):
        return {
            "is_valid": False,
            "message": "Image is invalid"
        }

    if content_type not in ALLOWED_IAMGE_TYPES:
        return {
                    "is_valid": False,
                    "message": "Image is invalid"
                }

    size = len(content)/(1024*1024)

    if size > 15:
        return {
                    "is_valid": False,
                    "message": "Image is invalid"
                }

    image = Image.open(io.BytesIO(content))
    width, height = image.size
     
    return{
                "is_valid": True,
                "message": "Image is valid",
                "width": width,
                "height": height,
                "size_mb": size
            }


# IMAGE RESIZING IF NEEDED
def resize_image_if_needed(content: bytes) ->bytes:
    image = Image.open(io.BytesIO(content))

    width, height = image.size

    if width <= MAX_IMAGE_DIMENSION and height <= MAX_IMAGE_DIMENSION:
        return content
    if width > height:
        new_width = MAX_IMAGE_DIMENSION
        new_height = int((MAX_IMAGE_DIMENSION / width) * height)
    else :
        new_height = MAX_IMAGE_DIMENSION
        new_width = int((MAX_IMAGE_DIMENSION / height) * width)

    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    output = io.BytesIO()
    resized_image.save(output, format=image.format)
    return output.getvalue()


# function to save the image
def save_image(content:bytes, upload_path:str, filename:str) ->str:
    os.makedirs(upload_path, exist_ok=True)
    file_path = os.path.join(upload_path, filename)
    
    with open(file_path, "wb") as  f:
        f.write(content)
    return file_path