from fastapi import FastAPI
from database import engine, Base
import models
from routers import users, debts, settings, monitoring

# Create tables (dev) — productionda alembic ishlatish tavsiya etiladi
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Debt Manager API")

# include routers
app.include_router(users.router)
app.include_router(debts.router)
app.include_router(settings.router)
app.include_router(monitoring.router)

@app.get("/")
def home():
    return {"message": "Debt Manager API ishlayapti"}
