from src.utils import utils
    
def analyze_sets(sets: int, fitness_goal: str) -> utils.AnalysisTip:
    if fitness_goal == "strength":
        return (
            "too_much" if sets > 6
            else "just_right" if sets >= 3
            else "too_low"
        )
    elif fitness_goal == "muscle_growth":
        return (
            "too_much" if sets > 5
            else "just_right" if sets >= 3
            else "too_low"
        )
    else:
        return (
            "too_much" if sets > 4
            else "just_right" if sets >= 2
            else "too_low"
        )
    
def analyze_reps(reps: int, fitness_goal: str) -> utils.AnalysisTip:
    if fitness_goal == "strength":
        return (
            "too_much" if reps > 6
            else "just_right" if reps >= 3
            else "too_low"
        )
    elif fitness_goal == "muscle_growth":
        return (
            "too_much" if reps > 12
            else "just_right" if reps >= 6
            else "too_low"
        )
    else:
        return (
            "too_much" if reps > 20
            else "just_right" if reps >= 12
            else "too_low"
        )
    
def analyze_rest_time(rest_time: int, fitness_goal: str) -> utils.AnalysisTip:
    if fitness_goal == "strength":
        return (
            "too_much" if rest_time > 300
            else "just_right" if rest_time >= 120
            else "too_low"
        )
    elif fitness_goal == "muscle_growth":
        return (
            "too_much" if rest_time > 90
            else "just_right" if rest_time >= 60
            else "too_low"
        )
    else:
        return (
            "too_much" if rest_time > 60
            else "just_right" if rest_time >= 30
            else "too_low"
        )
    
def analyze_weight(pr_weight: int, weight: int, fitness_goal: str) -> utils.AnalysisTip:
    weight_ratio = weight / pr_weight
    if fitness_goal == "strength":
        return (
            "too_much" if weight_ratio > .9
            else "just_right" if weight_ratio >= .85
            else "too_low"
        )
    elif fitness_goal == "muscle_growth":
        return (
            "too_much" if weight_ratio > .75
            else "just_right" if weight_ratio >= .65
            else "too_low"
        )
    else:
        return (
            "too_much" if weight_ratio > .6
            else "just_right" if weight_ratio >= .5
            else "too_low"
        )