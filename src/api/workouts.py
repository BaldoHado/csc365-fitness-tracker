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


@router.post("/{workout_name}")
def create_custom_workout(workout_name: str, muscle_group: str, equipment: str):
    """
    Adds a custom workout to our database.
    """
    with db.engine.begin() as connection:
        workout_exist = connection.execute(
            sqlalchemy.text(
                """
                SELECT 1 
                FROM workout
                WHERE LOWER(workout_name) = LOWER(:workout_name)
                """
            ),
            {"workout_name": workout_name},
        ).fetchall()
        if len(workout_exist):
            raise HTTPException(409, "Workout name already exists")
        muscle_exist = connection.execute(
            sqlalchemy.text(
                """
                SELECT muscle_group_id
                FROM muscle_group
                WHERE LOWER(muscle_group_name) = LOWER(:muscle_group_name)
                """
            ),
            {"muscle_group_name": muscle_group},
        ).first()
        muscle_id = (
            connection.execute(
                sqlalchemy.text(
                    """
                INSERT INTO muscle_group (muscle_group_name)
                VALUES (:muscle_group) RETURNING muscle_group_id
                """
                ),
                {"muscle_group": muscle_group},
            ).first()[0]
            if not muscle_exist
            else muscle_exist[0]
        )
        equipment_exist = connection.execute(
            sqlalchemy.text(
                """
                SELECT equipment_id
                FROM equipment
                WHERE LOWER(equipment_name) = LOWER(:equipment_name)
                """
            ),
            {"equipment_name": equipment},
        ).first()
        equipment_id = (
            connection.execute(
                sqlalchemy.text(
                    """
                INSERT INTO equipment (equipment_name)
                VALUES (:equipment_name)
                RETURNING equipment_id
                """
                ),
                {"equipment_name": equipment},
            ).first()[0]
            if not equipment_exist
            else equipment_exist[0]
        )
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO workout (workout_name, muscle_group_id, equipment_id) 
                VALUES (:workout_name, :muscle_id, :equipment_id)
                """
            ),
            {
                "workout_name": workout_name,
                "muscle_id": muscle_id,
                "equipment_id": equipment_id,
            },
        )
    return Response(content="Custom workout created.", status_code=201)


@router.get("/search/")
def find_workout(
    workout_name: str = None, muscle_group_name: str = None, equipment_name: str = None
):
    """
    Finds a workout given filter(s).
    """
    with db.engine.begin() as conn:
        present_args = {
            **({"workout_name": workout_name} if workout_name else {}),
            **({"muscle_group_name": muscle_group_name} if muscle_group_name else {}),
            **({"equipment_name": equipment_name} if equipment_name else {}),
        }
        if not present_args:
            raise HTTPException(400, "Pick a filter.")
        where_clause = ""
        for filter_name in present_args.keys():
            where_clause += f'{(" AND " if where_clause else "")} LOWER({filter_name}) = LOWER(:{filter_name})'
        print(where_clause)
        query = conn.execute(
            sqlalchemy.text(
                f"""
                SELECT workout_name, muscle_group.muscle_group_name, equipment.equipment_name
                FROM workout
                JOIN muscle_group ON muscle_group.muscle_group_id = workout.muscle_group_id
                JOIN equipment ON equipment.equipment_id = workout.equipment_id
                WHERE {where_clause}
                """
            ),
            present_args,
        ).fetchall()
        if not query:
            raise HTTPException(404, "Workout not found")
        return [
            {"workout_name": wrk_name, "muscle_group": mg_name, "equipment": e_name}
            for wrk_name, mg_name, e_name in query
        ]
