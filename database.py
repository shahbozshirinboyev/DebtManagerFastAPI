from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Get database URL from environment variable or use default for development
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/DebtManagerFastAPI"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=os.getenv("SQL_ECHO", "False").lower() == "true")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# get_db funksiyasi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
