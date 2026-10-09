from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from database import get_session

from models.user import User, ReadUser, CreateUser
from auth import verify_api_key

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=ReadUser)
def register_user(
    user_data: CreateUser,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)  # handles verification automatically
):
    
    existing = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already registered")

    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/", response_model=list[ReadUser])
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users 