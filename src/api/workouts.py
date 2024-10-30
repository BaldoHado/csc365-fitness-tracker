from fastapi import APIRouter, Depends
from src.api import auth
from src.utils import data_utils
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/")
def get_workouts():

    res = []
    with db.engine.begin() as connection:
        workouts = connection.execute(sqlalchemy.text("SELECT workout_name, muscle_group FROM workout")).fetchall()

        for i in range(len(workouts)):
            res.append({
                "name": workouts[i][0],
                "muscle_groups": workouts[i][1]
            },)

        return res
    

@router.post("/workouts/{workout_name}/{muscle_group}/{equipment}")
def add_custom_workout(workout_name: str, muscle_group: str, equipment: str):
    with db.engine.begin() as connection:
        workouts = connection.execute(sqlalchemy.text("SELECT workout_name FROM workout")).fetchall()
        print(workouts)

    existing_workouts = set(workout[0] for workout in workouts)
    
    if workout_name in existing_workouts:
        return []
    
    
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO workout (workout_name, muscle_group, equipment) VALUES (:workout_name, :muscle_group, :equipment)"), {"workout_name": workout_name, "muscle_group": muscle_group, "equipment": equipment})
    return [
        {
            "name": workout_name,
            "muscle_group": muscle_group,
            "equipment": equipment
        }
    ]
