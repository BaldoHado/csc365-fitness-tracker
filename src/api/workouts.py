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
        workouts = connection.execute(
            sqlalchemy.text("SELECT workout_name, muscle_group FROM workout")
        )

        for i in range(len(workouts)):
            res.append(
                {"name": workouts[i][0], "muscle_groups": workouts[i][1]},
            )

        return res


@router.get("/search/{workout_name}")
def find_workout(workout_name: str):
    with db.engine.begin() as conn:
        query = conn.execute(
            sqlalchemy.text(
                "SELECT workout_id, workout_name, muscle_group, equipment FROM workout WHERE LOWER(workout_name) = LOWER(:workout_name)"
            ),
            {"workout_name": workout_name},
        ).first()
        if not query:
            return {}
        return {
            "workout_id": query[0],
            "workout_name": query[1],
            "muscle_group": query[2],
            "equipment": query[3],
        }
