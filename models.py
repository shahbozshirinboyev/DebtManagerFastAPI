from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum

from database import Base

class DebtType(enum.Enum):
    owed_to = "owed_to"
    owed_by = "owed_by"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    settings = relationship("Setting", back_populates="user", uselist=False)
    debts = relationship("Debt", back_populates="user")

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    default_currency = Column(String, default="UZS")
    reminder_time = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="settings")

class Debt(Base):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    debt_type = Column(Enum(DebtType), nullable=False)
    person_name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, default="UZS")
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="debts")
