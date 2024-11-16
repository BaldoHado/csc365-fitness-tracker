from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
import sqlalchemy
from src import database as db
import src.api.workouts as workouts
import src.utils.utils as utils
from typing import List
from pydantic import PositiveInt, BaseModel

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.post("/{first_name}/{last_name}")
def post_user(first_name: str, last_name: str):
    """
    Inserts a new user into the database.
    Returns the user's id.
    """
    with db.engine.begin() as connection:
        (user_id,) = connection.execute(
            sqlalchemy.text(
                """INSERT INTO users (first_name, last_name)
                VALUES (:first_name, :last_name)
                RETURNING user_id"""
            ),
            {"first_name": first_name, "last_name": last_name},
        ).first()

    return {"user_id": user_id}


@router.put("/{user_id}/workouts/{workout_name}")
def update_user_workout(
    user_id: PositiveInt,
    workout_name: str,
    sets: PositiveInt = None,
    reps: PositiveInt = None,
    weight: PositiveInt = None,
    rest_time: PositiveInt = None,
    one_rep_max: PositiveInt = None,
):
    """
    Updates a workout in a user's account.
    """
    workout_id = workouts.find_workout(workout_name).get("workout_id", None)
    if not workout_id:
        raise HTTPException(status_code=404, detail="Workout not found")

    update_data = {}
    if sets is not None:
        update_data["sets"] = sets
    if reps is not None:
        update_data["reps"] = reps
    if weight is not None:
        update_data["weight"] = weight
    if rest_time is not None:
        update_data["rest_time"] = rest_time
    if one_rep_max is not None:
        update_data["one_rep_max"] = one_rep_max

    if len(update_data.keys()) == 0:
        raise HTTPException(status_code=400, detail="No update values provided")

    set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
    update_data["user_id"] = user_id
    update_data["workout_id"] = workout_id

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                f"UPDATE user_workout_item SET {set_clause} WHERE user_id = :user_id AND workout_id = :workout_id"
            ),
            update_data,
        )
    return "OK"


@router.post("/{user_id}/workouts/{workout_name}")
def post_workout_to_user(
    user_id: PositiveInt,
    workout_name: str,
    sets: PositiveInt,
    reps: PositiveInt,
    weight: PositiveInt,
    rest_time: PositiveInt,
    one_rep_max: PositiveInt,
):
    """
    Adds a new workout to a user's account.
    """
    workout_id = workouts.find_workout(workout_name).get("workout_id", None)
    if not workout_id:
        raise HTTPException(status_code=404, detail="Workout not found")
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO user_workout_item (user_id, workout_id, sets, reps, weight, rest_time, one_rep_max) 
                VALUES (:user_id, :workout_id, :sets, :reps, :weight, :rest_time, :one_rep_max)
                """
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
    return "OK"


@router.get("/{user_id}/workouts")
def get_workouts_from_user(user_id: PositiveInt) -> List[utils.NamedWorkoutItem]:
    """
    Returns all workouts from a user's account.
    """
    with db.engine.begin() as connection:
        workouts_db = connection.execute(
            sqlalchemy.text(
                """
                SELECT workout.workout_name,
                    u.sets,
                    u.reps,
                    u.weight,
                    u.rest_time,
                    u.one_rep_max
                FROM user_workout_item u
                JOIN workout ON workout.workout_id = u.workout_id
                WHERE user_id = :user_id
                """
            ),
            {"user_id": user_id},
        ).fetchall()

    if not workouts_db:
        return []
    return [
        utils.NamedWorkoutItem(
            workout_name=workout_name,
            sets=sets,
            reps=reps,
            weight=weight,
            rest_time=rest_time,
            one_rep_max=one_rep_max,
        )
        for workout_name, sets, reps, weight, rest_time, one_rep_max in workouts_db
    ]


@router.delete("/{user_id}/workouts")
def delete_workout_from_user(user_id: PositiveInt, workout_name: str):
    """
    Deletes a workout from a user's account.
    """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM user_workout_item 
                WHERE user_id = :user_id  AND workout_id IN (
                SELECT workout.workout_id
                FROM workout
                WHERE workout.workout_name = :workout_name)
                """
            ),
            {"workout_name": workout_name, "user_id": user_id},
        )

    return "OK"
