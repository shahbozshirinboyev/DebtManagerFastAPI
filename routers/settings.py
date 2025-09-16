from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_settings():
    return {"settings": {"currency": "UZS", "language": "uz"}}
