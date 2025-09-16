from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional
import crud, models, database, utils, schemas
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")
    
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username=username)
    if not user:
        return False
    if not utils.verify_password(password, user.password_hash):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Use our verify_token utility which handles both access and refresh tokens
        payload = utils.verify_token(token, is_refresh=False)
        username: str | None = payload.get("sub")
        if not username:
            raise credentials_exception
            
        user = crud.get_user_by_username(db, username=username)
        if user is None:
            raise credentials_exception
        return user
    except HTTPException as e:
        # Re-raise HTTP exceptions (like expired token)
        raise e
    except Exception as e:
        # Catch any other exceptions and return 401
        raise credentials_exception
