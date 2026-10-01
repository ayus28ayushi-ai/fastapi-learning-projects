from fastapi import FastAPI
from src.data import pincode_db
from src.exceptions import (
    PincodeNotFound, 
    pincode_not_found_handler, 
    InvalidPincode, 
    invalid_pincode_handler
    )
from src.models import LocationResponse, MultipleLocationRequest, MultipleLocationResponse


app=FastAPI(
    title="Pincode Lookup API",
    description="Auto fills city and state from Indian Pincodes"
)

#we have to register our custom exception handler
app.add_exception_handler(PincodeNotFound, pincode_not_found_handler)
app.add_exception_handler(InvalidPincode, invalid_pincode_handler)

@app.get("/")
def root():
    return {"message":"Pincode Loopup API"}


@app.post("/pincode/bulk", response_model=MultipleLocationResponse)
def get_bulk_locations(request: MultipleLocationRequest):
    results= []
    missing=[]

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)

    return MultipleLocationResponse(
        found=len(results),
        not_found=len(missing),
        results = results,
        missing = missing
    )

@app.get("/pincode/{code}", response_model=LocationResponse)
def get_location(code: str):
    if len(code) != 6 or not code.isdigit():
        raise InvalidPincode(code)

    if code not in pincode_db:
        raise PincodeNotFound(code)
    return pincode_db[code]


    
    