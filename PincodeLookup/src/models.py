from pydantic import BaseModel, field_validator

class PincodeRequest(BaseModel):
    pincode: str

    """classmethod tells python that this method belongs to the class blueprint itself
        and is not to specific object of the class. so the method can run even
            before the object exists 
    """

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value):
        if len(value) != 6 or not value.isdigit():
            raise ValueError("Pincode must be a 6 digit number")
        return value

class LocationResponse(BaseModel):
    pincode: str
    city: str
    district: str
    state: str

class MultipleLocationRequest(BaseModel):
    pincodes: list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls, values):
        if len(values) == 0:
            raise ValueError("Minimum one pincode required")
        if len(values) > 20:
            raise ValueError("Maximum 20 pincodes allowed")

        for code in values:
            if len(code) != 6 or not code.isdigit():
                raise ValueError("Pincode must be a 6 digit number")
        return values  

class MultipleLocationResponse(BaseModel):
    status: str="Success"
    found: int
    not_found: int
    results: list[LocationResponse]
    missing:list[str]