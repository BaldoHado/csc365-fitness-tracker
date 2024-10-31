from fastapi import APIRouter, Depends
from src.api import auth
from src.utils import data_utils
import sqlalchemy
from src import database as db
import src.api.workouts as workouts
import src.utils.utils as utils

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

@router.post("/{user_id}/workouts/{workout_name}")
def post_workout_to_user(user_id: str, workout_name: str, sets: int, reps: int, weight: int, rest_time: int, one_rep_max: int):
    workout_id = workouts.find_workout(workout_name)["workout_id"]
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "INSERT INTO user_workout_item (user_id, workout_id, sets, reps, weight, rest_time, one_rep_max) "
                "VALUES (:user_id, :workout_id, :sets, :reps, :weight, :rest_time, :one_rep_max)"
            ),
            {
                "user_id": user_id,
                "workout_id": workout_id,
                "sets": sets,
                "reps": reps,
                "weight": weight,
                "rest_time": rest_time,
                "one_rep_max": one_rep_max,
            },
        )
    return {
        "user_id": user_id,
        "workout_id": workout_id,
        "sets": sets,
        "reps": reps,
        "weight": weight,
        "rest_time": rest_time,
        "one_rep_max": one_rep_max,
    }

@router.get("/{user_id}/workouts")
def get_workouts_from_user(user_id: str):
    with db.engine.begin() as connection:
        workouts_db = connection.execute(
            sqlalchemy.text(
                "SELECT workout.workout_name, "
                        "u.sets, " 
                        "u.reps, "
                        "u.weight, "
                        "u.rest_time, " 
                        "u.one_rep_max "
                "FROM user_workout_item u "
                "JOIN workout on workout.workout_id = u.workout_id "
                "WHERE user_id = :user_id"    
            ),
            {"user_id": user_id},
        ).fetchall()
        
    workouts_list = [
        {
            "workout_name": row.workout_name,
            "sets": row.sets,
            "reps": row.reps,
            "weight": row.weight,
            "rest_time": row.rest_time,
            "one_rep_max": row.one_rep_max
        }
        for row in workouts_db
    ]

    return workouts_list