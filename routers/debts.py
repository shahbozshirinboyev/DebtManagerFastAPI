from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
import schemas, crud, database, auth

router = APIRouter(prefix="/api/debts", tags=["debts"])

@router.post("/", response_model=schemas.DebtResponse, status_code=201)
def add_debt(payload: schemas.DebtCreate, current_user = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    d = crud.create_debt(db, payload, current_user.id)
    return d

@router.put("/{debt_id}", response_model=schemas.DebtResponse)
def edit_debt(debt_id: int, payload: schemas.DebtUpdate, current_user = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    d = crud.update_debt(db, debt_id, current_user.id, payload)
    if not d:
        raise HTTPException(status_code=404, detail="Debt not found")
    return d

@router.delete("/{debt_id}", status_code=204)
def remove_debt(debt_id: int, current_user = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    ok = crud.delete_debt(db, debt_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Debt not found")
    return

@router.get("/", response_model=List[schemas.DebtResponse])
def list_debts(debt_type: Optional[str] = Query(None), current_user = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    debts = crud.get_user_debts(db, current_user.id, debt_type=debt_type)
    return debts
