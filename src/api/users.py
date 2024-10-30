from fastapi import APIRouter, Depends
from src.api import auth
from src.utils import data_utils
import sqlalchemy
from src import database as db
import src.api.workouts as workouts

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/{first_name}/{last_name}")
def post_user(first_name: str, last_name: str):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "INSERT INTO users (first_name, last_name) "
                "VALUES (:first_name, :last_name)"
            ),
            {"first_name": first_name, "last_name": last_name},
        )

    return {"first_name": first_name, "last_name": last_name}

@router.post("/{user_id}/workouts/{workout_name}/{sets}/{reps}/{weight}/{rest_time}/{one_rep_max}")
def post_workout_to_user(user_id: str, workout_name: str, sets: int, reps: int, weight: int, rest_time: int, one_rep_max: int):
    # workouts.find_workout()
    pass
