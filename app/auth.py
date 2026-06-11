from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database import SessionLocal
from app.crud import get_user_by_username


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str, 
    hashed_password: str,
):
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )
    
    
def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        username = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        return username
    
    except JWTError:
        raise credentials_exception
    
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    
    db = SessionLocal()
    
    try:
        user = get_user_by_username(db, username)
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    
    finally:
        db.close()