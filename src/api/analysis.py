from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.api import auth, users
import sqlalchemy
from src import database as db
from src.utils import analysis_utils, utils
from src.api import users
from typing import List, Dict, Union
from pydantic import PositiveInt
import json
import time

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
) -> Dict[str, Union[Dict[str, utils.AnalysisTip], str]]:
    """
    Returns tips for the workouts of a given user.
    Analyzes the sets, reps, weights, and rest time of each workout
    given a fitness goal.

    Time to execute: .126 ms
    """
    start = time.time()
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

    end = time.time()
    print("DURATION:  ", (end-start)*1000)
    return JSONResponse(
        content={
            "summary": (
                "When training for strength, focus on lifting as heavy as you can safely manage for a few powerful reps. Take longer rest periods to fully recover between sets and maintain maximum effort. Prioritize progressive overload and proper form to steadily build strength."
                if fitness_goal == "strength"
                else (
                    "When training for muscle growth, focus on moderate to heavy resistance and aim to push your muscles to near fatigue with controlled reps. Keep rest periods moderate to sustain intensity and build muscle. Consistency, progressive overload, and a mix of compound and isolation exercises are key."
                    if fitness_goal == "muscle_growth"
                    else "When training for endurance, focus on light to moderate resistance and aim to maximize your reps while maintaining proper form. Keep rest periods short to sustain effort and build stamina. Prioritize steady, controlled movements and consistency to enhance muscular and cardiovascular endurance."
                )
            ),
            "your_workouts": response,
        },
        status_code=200,
    )


@router.get("/users/{user_id}/distributions/", status_code=200)
def workout_distribution(
    user_id: PositiveInt,
    connection: sqlalchemy.Connection = Depends(db.get_db_connection),
) -> List[Dict[str, float]]:
    """
    Calculates the percent of workouts per muscle group
    for a given user.

    Planning Time: 0.605 ms
    Execution Time: 5.943 ms
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
