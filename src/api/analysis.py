from fastapi import APIRouter, Depends, HTTPException
from src.api import auth, users
import sqlalchemy
from src import database as db
from src.utils import analysis_utils, utils
from typing import List, Dict


router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("/{user_id}/tips/{fitness_goal}")
def get_workout_tips(
    user_id: str, fitness_goal: utils.FitnessGoal
) -> Dict[str, Dict[str, utils.AnalysisTip]]:
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
    """
    Calculates the percent of workouts per muscle group
    for a given user.
    """
    with db.engine.begin() as conn:
        query = conn.execute(
            sqlalchemy.text(
                """
                SELECT 
                    LOWER(workout.muscle_group) AS muscle_group, 
                    ROUND(COUNT(workout.muscle_group)::DECIMAL / 
                        (SELECT COUNT(*) 
                        FROM user_workout_item 
                        WHERE user_id = :user_id), 3) AS percentage
                FROM user_workout_item
                JOIN workout ON user_workout_item.workout_id = workout.workout_id
                WHERE user_id = :user_id
                GROUP BY muscle_group
                """
            ),
            {"id": user_id, "user_id": user_id},
        ).fetchall()
        if not query:
            raise HTTPException(
                status_code=404,
                detail=f"No workout data found for user with ID {user_id}.",
            )
    return [{name: val} for name, val in query]
