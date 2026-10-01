from pydantic import BaseModel

class CafeMenuItem(BaseModel):
    id:int
    name:str
    price:int
    category:str
    description:str
    available:bool

class MenuResponse(BaseModel):
    status: str="Success"
    count: int
    items: list[CafeMenuItem]