import sqlalchemy
from faker import Faker
import numpy as np
import os
import dotenv

def database_connection_url():
    dotenv.load_dotenv()
    return os.environ.get("POSTGRES_URI")


engine = sqlalchemy.create_engine(database_connection_url())

with engine.begin() as conn:
    # conn.execute(sqlalchemy.text("""
    #     DROP TABLE IF EXISTS users CASCADE;

    #     DROP TABLE IF EXISTS user_workout_item;
        
    #     create table
    #         public.users (
    #         user_id bigserial not null,
    #         first_name text not null,
    #         last_name text not null,
    #         constraint users_pkey primary key (user_id)
    #     ) tablespace pg_default;
                                 
    #     create table
    #         public.user_workout_item (
    #         user_id bigint not null,
    #         workout_id bigint not null,
    #         sets integer not null,
    #         reps integer not null,
    #         weight integer not null,
    #         rest_time integer not null,
    #         one_rep_max integer not null,
    #         constraint user_workout_item_pkey primary key (user_id, workout_id),
    #         constraint user_workout_item_user_id_fkey foreign key (user_id) references users (user_id),
    #         constraint user_workout_item_workout_id_fkey foreign key (workout_id) references workout (workout_id)
    #     ) tablespace pg_default;
                        
    # """))

    fake = Faker()

    num_users = 2124
    # user_data = [
    #     {"first_name": fake.first_name(),
    #         "last_name": fake.last_name()}
    #     for _ in range(num_users)
    #     ]
    
    num_workouts = 471
    assign_workout = []
    for user_id in range(1, num_users + 1):
        for workout_id in range(1, num_workouts + 1):
            assign_workout.append({
                "user_id": user_id,
                "workout_id": workout_id,
                "sets": np.random.randint(2, 10),
                "reps": np.random.randint(5, 20),
                "weight": np.random.randint(3, 300),
                "rest_time": np.random.randint(15, 300),
                "one_rep_max": np.random.randint(1, 400)
            })
    
    # conn.execute(sqlalchemy.text(
    #     """
    #     INSERT INTO users (first_name, last_name)
    #     VALUES (:first_name, :last_name)
    #     """
    #     ),
    #     user_data
    # )
    conn.execute(sqlalchemy.text(
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
    )

