from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

# Database connection URL - update this if your database credentials are different
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/DebtManagerFastAPI"

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Add the created_at column
    with engine.connect() as connection:
        # Check if column already exists
        result = connection.execute(
            text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='debts' AND column_name='created_at'
            """)
        ).fetchone()
        
        if not result:
            # Add the column if it doesn't exist
            connection.execute(
                text("""
                    ALTER TABLE debts 
                    ADD COLUMN created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                """)
            )
            connection.commit()
            print("✅ Successfully added 'created_at' column to 'debts' table")
        else:
            print("ℹ️ 'created_at' column already exists in 'debts' table")
            
except Exception as e:
    print(f"❌ Error: {e}")
    session.rollback()
finally:
    session.close()
