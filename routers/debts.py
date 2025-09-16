from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_debts():
    return {"debts": ["qarz1", "qarz2", "qarz3"]}

@router.post("/")
def create_debt(amount: float, description: str):
    return {"message": f"{amount} so'm qarz qo'shildi: {description}"}
