from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from src.api import auth
import sqlalchemy
from src import database as db
from faker import Faker
import numpy as random

def add_fake_data():
    
    """ Generates 2000 users to the database
        Uses faker to create names for each user """

    fake = Faker()

    num_users = 10
    user_data = [
        {"first_name": fake.first_name(),
         "last_name": fake.last_name()}
        for _ in range(num_users)
        ]
    
    num_workouts = 10
    assign_workout = [
        {"user_id": user_id,
          "workout_id": (user_id % num_workouts) or num_workouts,
          "sets": random.randint(1,5),
          "reps": random.rantint(5,20),
          "weight": random.randint(2,300),
          "rest_time": random.randint(15,600),
           "one_rep_max": random.randint(400) }
          for user_id in range(1, num_users + 1)
          ]
    print(user_data["first_name"])

    with db.engine.begin() as conn:
        conn.execute(sqlalchemy.text((
            """
            INSERT INTO users (first_name, last_name)
            VALUES (:first_name, :last_name)
            """
            ),
            user_data
        ))
        conn.execute(sqlalchemy.text((
            """
            INSERT INTO user_workout_item (
                user_id,
                workout_id,
                sets, 
                reps, 
                weight, 
                rest_time, 
                one_rep_max)
            VALUES (
                :user_id,
                :workout_id,
                :sets, 
                :reps, 
                :weight, 
                :rest_time, 
                :one_rep_max)
            """ 
            ),
            assign_workout
        ))
if __name__ == "__main__":
    add_fake_data
