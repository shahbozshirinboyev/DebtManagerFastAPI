from fastapi import FastAPI
from routers import auth, debts, settings, monitoring

app = FastAPI(title="DebtManager API")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(debts.router, prefix="/api/debts", tags=["Debts"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["Monitoring"])

@app.get("/")
def read_root():
    return {"message": "DebtManagerAPI is working... 🚀"}