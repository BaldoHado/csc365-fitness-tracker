from fastapi import APIRouter, Depends
from src.api import auth
from src.utils import data_utils

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/")
def post_user():
    return "OK"
