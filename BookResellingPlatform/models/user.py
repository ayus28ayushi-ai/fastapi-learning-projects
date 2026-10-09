from sqlmodel import SQLModel, Field, Relationship
from typing import Optional



# database table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email:str = Field(unique=True)
    college: str

    books: list["Books"] = Relationship(back_populates="owner")

# request body
class CreateUser(SQLModel):
    name: str
    email: str
    college: str

# response body
class ReadUser(SQLModel):
    id: int
    name: str
    email: str
    college: str


# to avoid circular imports
from models.books import Books
User.model_rebuild()