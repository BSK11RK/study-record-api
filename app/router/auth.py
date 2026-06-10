from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas import UserCreate, UserLogin, TokenResponse
from app.crud import create_user, get_user_by_username
from app.auth import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
        
@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    exists = get_user_by_username(db, user.username)
    
    if exists:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = hash_password(user.password)
    
    create_user(db, user.username, hashed_password)
    
    return {"message": "User created"}


@router.post("/login", response_model=TokenResponse)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = get_user_by_username(db, user.username)
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user.username})
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }