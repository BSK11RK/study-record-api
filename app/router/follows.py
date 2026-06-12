from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.auth import get_current_user
from app.models import User
from app.schemas import FollowResponse
from app.crud import (
    follow_user,
    unfollow_user,
    get_followers,
    get_following
)


router = APIRouter(prefix="/follows", tags=["Follows"])


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
        
@router.post("/{user_id}")
def follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = follow_user(db, current_user.id, user_id)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    return {"message": "followed"}


@router.delete("/{user_id}")
def unfollow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = unfollow_user(db, current_user.id, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Follow not found")
    
    return {"message": "unfollowed"}


@router.get("/followers/{user_id}", response_model=list[FollowResponse])
def followers(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_followers(db, user_id)


@router.get("/following/{user_id}", response_model=list[FollowResponse])
def following(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_following(db, user_id)