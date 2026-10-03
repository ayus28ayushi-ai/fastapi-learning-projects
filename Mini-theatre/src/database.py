from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///minitheatre.db"

engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    """The with statement is a safety guard. 
        It automatically opens a fresh session using your database engine,
         and guarantees that the session will be closed properly
        when you're finished—even if an error crashes your code halfway through."""
    with Session(engine) as session:
        yield session