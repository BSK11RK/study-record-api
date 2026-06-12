from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.auth import get_current_user
from app.crud import get_user_profile
from app.models import User
from app.schemas import UserProfileResponse, FollowResponse
from app.crud import (
    get_user_profile,
    follow_user,
    unfollow_user,
    get_followers,
    get_following
)


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


# フォロー
@router.post("/{user_id}/follow")
def follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = follow_user(db, current_user.id, user_id)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    return {"message": "followed"}


# アンフォロー
@router.delete("/{user_id}/follow")
def unfollow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = unfollow_user(db, current_user.id, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Follow not found")
    
    return {"message": "unfollowed"}


# Followers
@router.get("/{user_id}/followers", response_model=list[FollowResponse])
def followers(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_followers(db, user_id)


# Following
@router.get("/{user_id}/following", response_model=list[FollowResponse])
def following(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_following(db, user_id)