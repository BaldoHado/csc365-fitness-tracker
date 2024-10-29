from fastapi import APIRouter, Depends
from src.api import auth
from src.utils import data_utils
import sqlalchemy
from src import database as db
from src.utils import analysis_utils, utils
from typing import List

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("/{user_id}/tips/{fitness_goal}")
def get_workout_tips(user_id, fitness_goal):
    workout_items = [
        utils.WorkoutItem(
            "1", 4, [8, 7, 5, 4], [95, 145, 165, 170], [60, 120, 180, 240], 185
        ),
        utils.WorkoutItem(
            "1", 3, [5, 5, 8, 12], [45, 95, 145, 125], [0, 30, 60, 60], 145
        ),
    ]

    return get_workout_tips(workout_items, fitness_goal)


def get_workout_tips(
    workout_items: List[utils.WorkoutItem], fitness_goal: utils.FitnessGoal
):
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
