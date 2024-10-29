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

    res = []
    with db.engine.begin() as connection:
        workouts = connection.execute(sqlalchemy.text("SELECT workout_name, muscle_group FROM workout"))

        for i in range(len(workouts)):
            res.append({
                "name": workouts[i][0],
                "muscle_groups": workouts[i][1]
            },)

        return res
