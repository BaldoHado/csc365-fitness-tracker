from dataclasses import dataclass
from typing import List, Literal

FitnessGoal = Literal["strength", "muscle_growth", "endurance"]

AnalysisTip = Literal["too_much", "just_right", "too_low"]

@dataclass
class WorkoutItem:
    workout_id: str
    sets: int
    reps: List[int]
    weight: List[int]
    rest_time: List[int]
    one_rep_max: int