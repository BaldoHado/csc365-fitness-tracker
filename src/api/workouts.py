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
    with db.engine.begin() as connection:
        workouts = connection.execute(
            sqlalchemy.text("SELECT workout_name, muscle_group FROM workout")
        ).fetchall()

        return (
            [
                {"name": name, "muscle_group": muscle_group}
                for name, muscle_group in workouts
            ]
            if workouts
            else []
        )


@router.get("/{muscle_group}")
def get_workout_from_muscle_group(muscle_group: str):
    with db.engine.begin() as connection:
        workouts = connection.execute(
            sqlalchemy.text(
                "SELECT workout_name, muscle_group FROM workout WHERE LOWER(muscle_group) = LOWER(:muscle_group)"
            ),
            {"muscle_group": muscle_group},
        ).fetchall()
        if not workouts:
            return []
        else:
            return [{"name": name, "muscle_group": group} for name, group in workouts]


@router.post("/workouts/{workout_name}/{muscle_group}/{equipment}")
def post_custom_workout(workout_name: str, muscle_group: str, equipment: str):
    with db.engine.begin() as connection:
        workouts = connection.execute(
            sqlalchemy.text("SELECT workout_name FROM workout")
        ).fetchall()
        print(workouts)

    existing_workouts = set(workout[0] for workout in workouts)

    if workout_name in existing_workouts:
        return []

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "INSERT INTO workout (workout_name, muscle_group, equipment) VALUES (:workout_name, :muscle_group, :equipment)"
            ),
            {
                "workout_name": workout_name,
                "muscle_group": muscle_group,
                "equipment": equipment,
            },
        )
    return [
        {"name": workout_name, "muscle_group": muscle_group, "equipment": equipment}
    ]


@router.get("/search/{workout_name}")
def find_workout(workout_name: str):
    with db.engine.begin() as conn:
        query = conn.execute(
            sqlalchemy.text(
                "SELECT workout_id, workout_name, muscle_group, equipment FROM workout WHERE LOWER(workout_name) = LOWER(:workout_name)"
            ),
            {"workout_name": workout_name},
        ).first()
        if not query:
            return {}
        return {
            "workout_id": query[0],
            "workout_name": query[1],
            "muscle_group": query[2],
            "equipment": query[3],
        }
