CREATE TABLE users (
    user_id bigserial NOT NULL PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL
);

CREATE TABLE user_workout_item (
    user_id bigint REFERENCES users (user_id),
    workout_id bigint REFERENCES workout (workout_id),
    sets int NOT NULL,
    reps int NOT NULL,
    weight int NOT NULL,
    rest_time int NOT NULL,
    one_rep_max int NOT NULL,
    PRIMARY KEY (user_id, workout_id) 
);

CREATE TABLE workout (
    workout_id bigserial NOT NULL PRIMARY KEY,
    workout_name text NOT NULL,
    muscle_group text NOT NULL,
    equipment text NOT NULL
);
