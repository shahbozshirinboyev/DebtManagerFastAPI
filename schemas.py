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
class Token(BaseModel):
    access_token: str
    token_type: str


# --- Debt ---
class DebtBase(BaseModel):
    amount: float
    description: Optional[str] = None


class DebtCreate(DebtBase):
    pass


class DebtUpdate(DebtBase):
    is_paid: Optional[bool] = None


class DebtResponse(DebtBase):
    id: int
    user_id: int
    is_paid: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Setting ---
class SettingBase(BaseModel):
    notifications_enabled: bool = True
    # theme uchun Optional bo'lishi shart emas — default "light"
    theme: str = "light"


class SettingCreate(SettingBase):
    pass


class SettingUpdate(SettingBase):
    pass


class SettingResponse(SettingBase):
    id: int
    user_id: int

    model_config = {"from_attributes": True}
