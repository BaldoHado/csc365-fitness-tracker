from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("/")
def get_workouts():
    """
    Gets all workouts in our database.
    """
    with db.engine.begin() as connection:
        workouts = connection.execute(
            sqlalchemy.text("SELECT workout_name, muscle_group FROM workout")
        ).fetchall()
        if not len(workouts):
            raise HTTPException(500, "Unknown Error")
        return [
            {"name": name, "muscle_group": muscle_group}
            for name, muscle_group in workouts
        ]


@router.get("/{muscle_group}")
def get_workout_from_muscle_group(muscle_group: str):
    """
    Gets all workouts in our database that work a given muscle group.
    """
    with db.engine.begin() as connection:
        workouts = connection.execute(
            sqlalchemy.text(
                "SELECT workout_name, muscle_group FROM workout WHERE LOWER(muscle_group) = LOWER(:muscle_group)"
            ),
            {"muscle_group": muscle_group},
        ).fetchall()
        if not workouts:
            raise HTTPException(404, "Muscle group not found")
        else:
            return [{"name": name, "muscle_group": group} for name, group in workouts]


@router.post("/workouts/{workout_name}")
def create_custom_workout(workout_name: str, muscle_group: str, equipment: str):
    """
    Adds a custom workout to our database.
    """
    with db.engine.begin() as connection:
        workouts = connection.execute(
            sqlalchemy.text(
                "SELECT 1 FROM workout WHERE LOWER(workout_name) = LOWER(:workout_name)"
            ),
            {"workout_name": workout_name},
        ).fetchall()
        if len(workouts):
            raise HTTPException(409, "Workout name already exists")
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
    return Response(content="Custom workout created.", status_code=201)


@router.get("/search/{workout_name}")
def find_workout(workout_name: str):
    """
    Finds data about a given workout.
    """
    with db.engine.begin() as conn:
        query = conn.execute(
            sqlalchemy.text(
                "SELECT workout_id, workout_name, muscle_group, equipment FROM workout WHERE LOWER(workout_name) = LOWER(:workout_name)"
            ),
            {"workout_name": workout_name},
        ).first()
        if not query:
            raise HTTPException(404, "Workout not found")
        return {
            "workout_id": query[0],
            "workout_name": query[1],
            "muscle_group": query[2],
            "equipment": query[3],
        }
