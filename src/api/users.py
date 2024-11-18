from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from src.api import auth
import sqlalchemy
from src import database as db
import src.api.workouts as workouts
import src.utils.utils as utils
from typing import List
from pydantic import PositiveInt

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.post("/")
def post_user(
    first_name: str,
    last_name: str,
    connection: sqlalchemy.Connection = Depends(db.get_db_connection),
):
    """
    Inserts a new user into the database.
    Returns the user's id.
    """
    insert_query = connection.execute(
        sqlalchemy.text(
            """
            INSERT INTO users (first_name, last_name)
            VALUES (:first_name, :last_name)
            RETURNING user_id
            """
        ),
        {"first_name": first_name, "last_name": last_name},
    ).first()
    if not insert_query:
        raise HTTPException(500, "Unable to insert into table. Unknown error")

    return JSONResponse(content={"user_id": insert_query[0]}, status_code=201)


@router.put("/{user_id}/workouts/{workout_id}")
def update_user_workout(
    user_id: PositiveInt,
    workout_id: PositiveInt,
    sets: PositiveInt = None,
    reps: PositiveInt = None,
    weight: PositiveInt = None,
    rest_time: PositiveInt = None,
    one_rep_max: PositiveInt = None,
    connection: sqlalchemy.Connection = Depends(db.get_db_connection),
):
    """
    Updates a workout in a user's account.
    """
    workouts.find_workout(workout_id, conn=connection)

    update_data = {}
    if sets:
        update_data["sets"] = sets
    if reps:
        update_data["reps"] = reps
    if weight:
        update_data["weight"] = weight
    if rest_time:
        update_data["rest_time"] = rest_time
    if one_rep_max:
        update_data["one_rep_max"] = one_rep_max

    if len(update_data.keys()) == 0:
        raise HTTPException(status_code=400, detail="No update values provided")

    set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
    update_data["user_id"] = user_id
    update_data["workout_id"] = workout_id

    connection.execute(
        sqlalchemy.text(
            f"UPDATE user_workout_item SET {set_clause} WHERE user_id = :user_id AND workout_id = :workout_id"
        ),
        update_data,
    )
    return Response(content="Workout updated successfully.", status_code=200)


@router.post("/{user_id}/workouts/{workout_name}")
def post_workout_to_user(
    user_id: PositiveInt,
    workout_id: PositiveInt,
    sets: PositiveInt,
    reps: PositiveInt,
    weight: PositiveInt,
    rest_time: PositiveInt,
    one_rep_max: PositiveInt,
    connection: sqlalchemy.Connection = Depends(db.get_db_connection),
):
    """
    Adds a new workout to a user's account.
    """
    workouts.find_workout(workout_id, conn=connection)

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
    return Response(content="Workout added to user successfully.", status_code=201)


@router.get("/{user_id}/workouts")
def get_workouts_from_user(
    user_id: PositiveInt,
    workout_id: PositiveInt = None,
    connection: sqlalchemy.Connection = Depends(db.get_db_connection),
) -> List[utils.WorkoutItem]:
    """
    Returns workouts from a user's account. If a workout_name is specified,
    returns info about the specific workout.
    """
    workouts_db = connection.execute(
        sqlalchemy.text(
            f"""
            SELECT workout.workout_name,
                u.sets,
                u.reps,
                u.weight,
                u.rest_time,
                u.one_rep_max
            FROM user_workout_item u
            JOIN workout ON workout.workout_id = u.workout_id
            WHERE user_id = :user_id {"AND u.workout_id = :workout_id" if workout_id else ''}
            """
        ),
        {"user_id": user_id, "workout_id": workout_id},
    ).fetchall()

    if not workouts_db:
        raise HTTPException(
            status_code=404,
            detail=f"No workout data found for user with ID {user_id}.",
        )
    return JSONResponse(
        content=[
            utils.WorkoutItem(
                workout_name=workout_name,
                sets=sets,
                reps=reps,
                weight=weight,
                rest_time=rest_time,
                one_rep_max=one_rep_max,
            )
            for workout_name, sets, reps, weight, rest_time, one_rep_max in workouts_db
        ],
        status_code=200,
    )


@router.delete("/{user_id}/workouts")
def delete_workout_from_user(
    user_id: PositiveInt,
    workout_id: PositiveInt,
    connection: sqlalchemy.Connection = Depends(db.get_db_connection),
):
    """
    Deletes a workout from a user's account.
    """
    get_workouts_from_user(user_id, workout_id, connection=connection)
    connection.execute(
        sqlalchemy.text(
            """
            DELETE FROM user_workout_item
            WHERE user_id = :user_id  AND workout_id = :workout_id
            """
        ),
        {"user_id": user_id, "workout_id": workout_id},
    )

    return Response(content="Workout deleted succesfully.", status_code=200)
