from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import schemas, crud, database, utils, models
from utils import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if username already exists
    existing_user = db.query(models.User).filter(models.User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists (if provided)
    if user_in.email:
        existing_email = db.query(models.User).filter(models.User.email == user_in.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the user
    user = crud.create_user(db, user_in)
    return user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(login_data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    # Find user by username
    user = crud.get_user_by_username(db, username=login_data.username)
    if not user or not utils.verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Create token with username as subject
    access_token = create_access_token(subject=user.username)
    return {"access_token": access_token, "token_type": "bearer"}
