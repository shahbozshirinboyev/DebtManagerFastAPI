# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# --- User ---
class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    # Pydantic v2 -- allow ORM objects
    model_config = {"from_attributes": True}


# --- Token ---
class TokenBase(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None

class Token(TokenBase):
    pass

class TokenResponse(TokenBase):
    """Response model for token endpoints"""
    pass

class RefreshToken(BaseModel):
    refresh_token: str


# --- Debt ---
class DebtBase(BaseModel):
    person_name: str
    amount: float
    currency: str = "UZS"
    description: Optional[str] = None
    debt_type: str  # 'owed_to' or 'owed_by'
    due_date: Optional[datetime] = None


class DebtCreate(DebtBase):
    pass


class DebtUpdate(BaseModel):
    person_name: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    debt_type: Optional[str] = None  # 'owed_to' or 'owed_by'
    due_date: Optional[datetime] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "person_name": "John Doe",
                "amount": 100000,
                "currency": "UZS",
                "description": "Qarz haqida izoh",
                "debt_type": "owed_to",
                "due_date": "2025-12-31T23:59:59"
            }
        }
    }


class DebtResponse(DebtBase):
    id: int
    user_id: int
    created_at: datetime
    start_date: datetime
    due_date: Optional[datetime] = None

    model_config = {"from_attributes": True}


# --- Setting ---
class SettingBase(BaseModel):
    notifications_enabled: bool = True
    theme: str = "light"
    default_currency: str = "UZS"
    reminder_time: Optional[datetime] = None
    reminder_enabled: bool = False


class SettingCreate(SettingBase):
    pass


class SettingUpdate(BaseModel):
    notifications_enabled: Optional[bool] = None
    theme: Optional[str] = None
    default_currency: Optional[str] = None
    reminder_time: Optional[datetime] = None
    reminder_enabled: Optional[bool] = None


class SettingResponse(SettingBase):
    id: int
    user_id: int
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 1,
                "notifications_enabled": True,
                "theme": "light"
            }
        }
    }
