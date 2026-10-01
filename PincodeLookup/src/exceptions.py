from fastapi.responses import JSONResponse
from fastapi import Request

class PincodeNotFound(Exception):
    def __init__(self, pincode: str):
       self.pincode = pincode

class InvalidPincode(Exception):
    def __init__(self, pincode: str, reason: str="Invalid Format"):
        self.pincode = pincode
        self.reason = reason

# custom hanndlers
async def pincode_not_found_handler(request:Request, exc: PincodeNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "error":"pincode not found",
            "message": f"No location available for pincode {exc.pincode}",
            "pincode": exc.pincode
        }
    )

async def invalid_pincode_handler(request:Request, exc:InvalidPincode):
    return JSONResponse(
        status_code=404,
        content={
            "error":"invalid pincode",
            "message": f"Pincode is invalid",
            "pincode": exc.pincode
        }
    )