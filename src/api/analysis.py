from fastapi import APIRouter, Depends
from src.api import auth, users
from src.utils import data_utils
import sqlalchemy
from src import database as db
from src.utils import analysis_utils, utils
from typing import List, Dict
from collections import Counter

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("/{user_id}/tips/{fitness_goal}")
def get_workout_tips(
    user_id: str, fitness_goal: utils.FitnessGoal
) -> List[Dict[str, utils.AnalysisTip]]:
    workout_items = users.get_workouts_from_user(user_id)
    response = {}
    for workout_item in workout_items:
        response[workout_item.workout_name] = {
            "sets": analysis_utils.analyze_sets(workout_item.sets, fitness_goal),
            "reps": analysis_utils.analyze_reps(workout_item.reps, fitness_goal),
            "weight": analysis_utils.analyze_weight(
                workout_item.one_rep_max, workout_item.weight, fitness_goal
            ),
            "rest_time": analysis_utils.analyze_rest_time(
                workout_item.rest_time, fitness_goal
            ),
        }
    return response


@router.post("/{user_id}/distribution/")
def workout_distribution(user_id: str) -> List[Dict[str, float]]:
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
