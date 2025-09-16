from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database, auth

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/", response_model=schemas.SettingResponse)
def read_settings(current_user = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    s = crud.get_setting(db, current_user.id)
    if not s:
        raise HTTPException(status_code=404, detail="Settings not found")
    return s

@router.patch("/", response_model=schemas.SettingResponse)
def update_settings(payload: schemas.SettingUpdate, current_user = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    s = crud.upsert_setting(db, current_user.id, payload)
    return s
