from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.auth import get_current_user
from app.crud import get_user_profile
from app.models import User
from app.schemas import UserProfileResponse


router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        

@router.get("/me", response_model=UserProfileResponse)
def read_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = get_user_profile(db, current_user.id)
    
    return profile


@router.get("/{user_id}", response_model=UserProfileResponse)
def read_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
):
    profile = get_user_profile(db, user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    
    return profile