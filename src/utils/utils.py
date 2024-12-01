from typing_extensions import List, Literal, TypedDict
from pydantic import PositiveInt

FitnessGoal = Literal["strength", "muscle_growth", "endurance"]

AnalysisTip = Literal["too_much", "just_right", "too_low"]


class WorkoutItem(TypedDict):
    workout_id: PositiveInt
    workout_name: str
    sets: int
    reps: List[int]
    weight: List[int]
    rest_time: List[int]
    one_rep_max: int
