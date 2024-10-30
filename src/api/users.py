from fastapi import APIRouter, Depends
from src.api import auth
from src.utils import data_utils
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/{first_name}/{last_name}")
def post_user(first_name: str, last_name: str):
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                "INSERT INTO users (first_name, last_name) "
                "VALUES (:first_name, :last_name)"
            ),
            {"first_name": first_name, "last_name": last_name},
        )

    return {"first_name": first_name, "last_name": last_name}

# adds a workout to the users id 
@router.post("/")
def post_workouts(user_list: list):
#  select workouts associated with user id from workout_item 
# output all of those workouts 
    # with db.engine.begin() as connection:
    #     connection.execute(sqlalchemy.text("UPDATE users SET first_name"))

    return "OK"
