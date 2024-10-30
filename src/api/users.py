from fastapi import APIRouter, Depends
from src.api import auth
from src.utils import data_utils
import sqlalchemy
from src import database as db
import src.api.workouts as workouts
import utils.utils as utils

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/users/{first_name}/{last_name}")
def post_user(first_name: str, last_name: str):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "INSERT INTO users (first_name, last_name) "
                "VALUES (:first_name, :last_name)"
            ),
            {"first_name": first_name, "last_name": last_name}
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
            {"user_id" :user_id, "workout_id":workout_id, "sets":sets, "reps":reps, "weight":weight,
              "rest_time":rest_time, "one_rep_max":one_rep_max}
        )
    return {
        "user_id": user_id,
        "workout_id":workout_id,
        "sets":sets,
        "reps":reps,
        "weight":weight,
        "rest_time":rest_time,
         "one_rep_max":one_rep_max
    
    }
@router.get("/{user_id}/workouts/")
def get_user_workouts(user_id):
    with db.engine.begin() as connection:
        db_workouts =  connection.execute(sqlalchemy.text(
            "SELECT user_id, workout_id, sets, reps, weight, rest_time, one_rep_max "
                                      "FROM user_workout_item "
                                      "WHERE user_id = :user_id"),
                                      {"user_id":user_id}
        ).fetchall()

        # workout_ids = for row in db_workouts

        # logic here to find workout name 
        workout_name = connection.execute(sqlalchemy.text(
            "SELECT workout_name FROM workouts "
            "WHERE workout_id = :workout_id"),
                                      {"workout_id":workout_id}
        )
        list_workouts = []
        for row in db_workouts: 
            workout = utils.WorkoutItem(
                sets = row.set
            )
            list_workouts.append(workout)

            
    return workouts
# user_id, workout_id, sets, reps, weight, rest_time, one_rep_max
