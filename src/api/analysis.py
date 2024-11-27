from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.api import auth, users
import sqlalchemy
from src import database as db
from src.utils import analysis_utils, utils
from src.api import users
from typing import List, Dict
from pydantic import PositiveInt
import json


router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("/users/{user_id}/tips/{fitness_goal}", status_code=200)
def get_workout_tips(
    user_id: PositiveInt,
    fitness_goal: utils.FitnessGoal,
    connection: sqlalchemy.Connection = Depends(db.get_db_connection),
) -> Dict[str, Dict[str, utils.AnalysisTip]]:
    """
    Returns tips for the workouts of a given user.
    Analyzes the sets, reps, weights, and rest time of each workout
    given a fitness goal.
    """
    users.find_user(user_id, connection=connection)
    workout_items = json.loads(
        users.get_workouts_from_user(user_id, connection=connection).body.decode(
            "utf-8"
        )
    )

    response = {}
    for workout_item in workout_items:
        response[workout_item["workout_name"]] = {
            "sets": analysis_utils.analyze_sets(workout_item["sets"], fitness_goal),
            "reps": analysis_utils.analyze_reps(workout_item["reps"], fitness_goal),
            "weight": analysis_utils.analyze_weight(
                workout_item["one_rep_max"], workout_item["weight"], fitness_goal
            ),
            "rest_time": analysis_utils.analyze_rest_time(
                workout_item["rest_time"], fitness_goal
            ),
        }

    return JSONResponse(content=response, status_code=200)


@router.get("/users/{user_id}/distributions/", status_code=200)
def workout_distribution(
    user_id: PositiveInt,
    connection: sqlalchemy.Connection = Depends(db.get_db_connection),
) -> List[Dict[str, float]]:
    """
    Calculates the percent of workouts per muscle group
    for a given user.
    """
    users.find_user(user_id, connection=connection)
    query = connection.execute(
        sqlalchemy.text(
            """
            SELECT 
                LOWER(muscle_group.muscle_group_name) AS muscle_group, 
                ROUND(COUNT(muscle_group.muscle_group_name)::DECIMAL / 
                    (SELECT COUNT(*) 
                    FROM user_workout_item 
                    WHERE user_id = :user_id), 3) AS percentage
            FROM user_workout_item
            JOIN workout ON user_workout_item.workout_id = workout.workout_id
            JOIN muscle_group ON muscle_group.muscle_group_id = workout.muscle_group_id
            WHERE user_id = :user_id
            GROUP BY muscle_group
            """
        ),
        {"user_id": user_id},
    ).fetchall()

    return JSONResponse(
        content=[{name: float(val)} for name, val in query], status_code=200
    )
