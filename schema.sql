CREATE TABLE muscle_groups (
    muscle_id bigserial NOT NULL PRIMARY KEY,
    muscle_name text NOT NULL
);

CREATE TABLE users (
    user_id bigserial NOT NULL PRIMARY KEY
);

CREATE TABLE workout_item (
    workout_id bigserial NOT NULL PRIMARY KEY,
    sets int NOT NULL,
    reps int NOT NULL,
    weight int NOT NULL,
    rest_time int NOT NULL,
    muscle_id bigint REFERENCES muscle_groups (muscle_id)
);

CREATE TABLE user_workout_item (
    user_id bigint REFERENCES users (user_id),
    workout_item_id bigint REFERENCES workout_item (workout_id),
    PRIMARY KEY (user_id, workout_item_id)
);

CREATE TABLE workout (
    workout_id bigserial NOT NULL PRIMARY KEY,
    workout_name text NOT NULL
);
