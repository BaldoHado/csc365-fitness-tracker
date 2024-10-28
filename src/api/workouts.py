from fastapi import APIRouter, Depends
from src.api import auth
from src.utils import data_utils

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/")
def get_workouts():
    return data_utils.read_data("./src/data/exercises.xlsx")
