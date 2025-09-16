from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, database, auth

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])

@router.get("/")
def monitoring_summary(current_user = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    summary = crud.get_monitoring_summary(db, current_user.id)
    return {"summary": summary}
