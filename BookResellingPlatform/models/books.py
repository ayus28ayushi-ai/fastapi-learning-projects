from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


# db table
class Books(SQLModel, table=True):
    id:Optional[int] = Field(default=True, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price : int
    is_sold: bool = Field(default=False)

    #foreign key
    user_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="books")


# request body
class BookCreate(SQLModel):
    title: str
    author: str
    price: str
    user_id: int

# response body
class BodyRead(SQLModel):
    id:int
    title: str
    author: str
    price: int
    is_sold: bool
    user_id: int 

class BookUpdate(SQLModel):
    price: Optional[int] = None
    is_sold : Optional[bool] = None

    
# avoiding the circular imports
from models.user import User
Books.model_rebuild()