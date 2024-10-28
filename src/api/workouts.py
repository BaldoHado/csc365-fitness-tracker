from fastapi import APIRouter, Depends
from src.api import auth
from src.utils import data_utils
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/")
def get_workouts():
     with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT * FROM global_inventory"))
        return data_utils.read_data("./src/data/exercises.xlsx")
