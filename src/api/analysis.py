from fastapi import APIRouter, Depends
from src.api import auth
from src.utils import data_utils
import sqlalchemy
from src import database as db
from src.utils import analysis_utils, utils
from typing import List
from collections import Counter

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("/{user_id}/tips/{fitness_goal}")
def get_workout_tips(user_id: str, fitness_goal: str):
    # Internal logic to fetch workout_items from a given user_id
    workout_items = [
        utils.WorkoutItem(
            "1", 4, [8, 7, 5, 4], [95, 145, 165, 170], [60, 120, 180, 240], 185
        ),
        utils.WorkoutItem(
            "1", 3, [5, 5, 8, 12], [45, 95, 145, 125], [0, 30, 60, 60], 145
        ),
    ]

    response = []
    for workout_item in workout_items:
        response.append(
            {
                "sets": analysis_utils.analyze_sets(workout_item.sets, fitness_goal),
                "reps": [
                    analysis_utils.analyze_reps(rep, fitness_goal)
                    for rep in workout_item.reps
                ],
                "weight": [
                    analysis_utils.analyze_weight(
                        workout_item.one_rep_max, weight, fitness_goal
                    )
                    for weight in workout_item.weight
                ],
                "rest_time": [
                    analysis_utils.analyze_rest_time(time, fitness_goal)
                    for time in workout_item.rest_time
                ],
            }
        )
    return response


@router.post("/{user_id}/distribution/")
def workout_distribution(user_id: str):
    with db.engine.begin() as conn:
        query = conn.execute(
            sqlalchemy.text(
                """
                WITH TotalWorkouts AS (
                    SELECT COUNT(workout_id) AS workout_count
                    FROM user_workout_item
                    WHERE user_id = :id
                )
                SELECT workout.workout_name, ROUND(COUNT(workout.muscle_group)::DECIMAL / (SELECT workout_count FROM TotalWorkouts), 4) AS percentage
                FROM user_workout_item
                JOIN workout ON user_workout_item.workout_id = workout.workout_id
                WHERE user_id = :user_id
                GROUP BY workout.workout_name
                """
            ),
            {"id": user_id, "user_id": user_id},
        ).fetchall()
        if not query:
            return []
        query = [{name: val} for name, val in query]
    return query
