from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.api import auth
import sqlalchemy
from src import database as db
from pydantic import PositiveInt


router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("/", status_code=200)
def get_workouts(connection: sqlalchemy.Connection = Depends(db.get_db_connection)):
    """
    Gets all workouts in the database.
    """
    workouts = connection.execute(
        sqlalchemy.text(
            """
            SELECT workout_id, workout_name, muscle_group_name, equipment_name
            FROM workout
            JOIN muscle_group ON workout.muscle_group_id = muscle_group.muscle_group_id
            JOIN equipment ON equipment.equipment_id = workout.equipment_id
            """
        )
    ).fetchall()
    if not len(workouts):
        raise HTTPException(500, "Unknown Error")
    return JSONResponse(
        content=[
            {
                "workout_id": wk_id,
                "workout_name": wk_name,
                "muscle_group_name": mg_name,
                "equipment_name": e_name,
            }
            for wk_id, wk_name, mg_name, e_name in workouts
        ],
        status_code=200,
    )


@router.post("/{workout_name}", status_code=201)
def create_custom_workout(
    workout_name: str,
    muscle_group: str,
    equipment: str,
    connection: sqlalchemy.Connection = Depends(db.get_db_connection),
):
    """
    Adds a custom workout to the database.
    """
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
    new_workout_id = connection.execute(
        sqlalchemy.text(
            """
            INSERT INTO workout (workout_name, muscle_group_id, equipment_id) 
            VALUES (:workout_name, :muscle_id, :equipment_id)
            RETURNING workout_id
            """
        ),
        {
            "workout_name": workout_name,
            "muscle_id": muscle_id,
            "equipment_id": equipment_id,
        },
    ).first()[0]
    return JSONResponse({"workout_id": new_workout_id}, 201)


@router.get("/search/", status_code=200)
def find_workout(
    workout_id: PositiveInt = None,
    workout_name: str = None,
    muscle_group_name: str = None,
    equipment_name: str = None,
    connection: sqlalchemy.Connection = Depends(db.get_db_connection),
):
    """
    Finds a workout given filter(s).
    """
    if not (
        present_args := {
            **({"workout_id": workout_id} if workout_id else {}),
            **({"workout_name": workout_name} if workout_name else {}),
            **({"muscle_group_name": muscle_group_name} if muscle_group_name else {}),
            **({"equipment_name": equipment_name} if equipment_name else {}),
        }
    ):
        raise HTTPException(400, "Pick a filter.")
    where_clause = ""
    for filter_name in present_args.keys():
        if filter_name == "workout_id":
            where_clause += (
                f'{(" AND " if where_clause else "")} {filter_name} = :{filter_name}'
            )
        else:
            where_clause += f'{(" AND " if where_clause else "")} LOWER({filter_name}) = LOWER(:{filter_name})'
    query = connection.execute(
        sqlalchemy.text(
            f"""
            SELECT workout_id, workout_name, muscle_group.muscle_group_name, equipment.equipment_name
            FROM workout
            JOIN muscle_group ON muscle_group.muscle_group_id = workout.muscle_group_id
            JOIN equipment ON equipment.equipment_id = workout.equipment_id
            WHERE {where_clause}
            """
        ),
        present_args,
    ).fetchall()
    if not query:
        raise HTTPException(status_code=404, detail="Workout not found")
    return JSONResponse(
        content=[
            {
                "workout_id": wrk_id,
                "workout_name": wrk_name,
                "muscle_group": mg_name,
                "equipment": e_name,
            }
            for wrk_id, wrk_name, mg_name, e_name in query
        ],
        status_code=200,
    )
