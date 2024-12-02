# Performance Tuning

## 1). FOR update_user_workout ENDPOINT:

I run explain analyze to see what the time it takes to run is:

```
EXPLAIN ANALYZE
INSERT INTO user_workout_item (user_id, workout_id, sets, reps, weight, rest_time, one_rep_max)
VALUES (123, 456, 3, 12, 100, 60, 120)
ON CONFLICT (user_id, workout_id)
DO UPDATE SET
    sets = EXCLUDED.sets,
    reps = EXCLUDED.reps,
    weight = EXCLUDED.weight,
    rest_time = EXCLUDED.rest_time,
    one_rep_max = EXCLUDED.one_rep_max;

```


I get a planning time of 1.33ms and execution time of 3.218ms

I  make sure the table has an index on user_id and workout_id by doing: 

```
CREATE UNIQUE INDEX idx_user_workout ON user_workout_item (user_id, workout_id);
```

After this I run explain analyze again from above and get

### INSERT FIRST SUPABASE IMAGE HERE



Conclusion: The added indices improved the speed of planning time by 1.154ms and the execution time by 1.715ms.

It was originally slow because the database had to scan all rows in the table to check if a user_id and workout_id already existed (sequential scan). This is very slow with a million rows because it processes each row one by one.

These indices were chosen because adding them on user_id and workout_id allows the database to quickly locate specific rows instead of scanning the whole table. This speeds up conflict resolution and filtering, making both inserts and updates much faster. 



Extra: 
I used this query to check if a row exists and add information if it does not. This was also good to test the endpoint with modified sql and see that it doesn’t allow multiple of the same workout

```
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM user_workout_item
        WHERE user_id = 123 AND workout_id = 456
    ) THEN
        INSERT INTO user_workout_item (user_id, workout_id, sets, reps, weight, rest_time, one_rep_max)
        VALUES (123, 456, 3, 12, 100, 60, 120);
    END IF;
END $$;
```


Then check the existing data by using this query: 

```
SELECT *
FROM user_workout_item
WHERE user_id = 123 AND workout_id = 456;
```

Where it returns

### INSERT SECOND SUPABASE IMAGE HERE


## 2). FOR post_workout_to_user  ENDPOINT:

I use the following query to add a workout and test it’s speed: 

```
EXPLAIN ANALYZE
INSERT INTO user_workout_item (user_id, workout_id, sets, reps, weight, rest_time, one_rep_max)
VALUES (1, 1, 3, 12, 100, 60, 120);
```

This is the response where planning time is .058ms and execution time is 2.603ms: 

### INSERT THIRD SUPBASE IMAGE HERE

I delete the workout from the user from:
https://csc365-fitness-tracker-1.onrender.com/docs#/users/get_workouts_from_user_users__user_id__workouts_get

Then I check which indexes exist by running: 

```
SELECT *
FROM pg_indexes
WHERE tablename IN ('users', 'workout');
```

And then running the following i find that there is only one index:

```
SELECT *
FROM pg_indexes
WHERE tablename = 'workout';
```

I add the following indexes: 

```
CREATE INDEX idx_workout_name ON workout (workout_name);
CREATE INDEX idx_muscle_group_id ON workout (muscle_group_id);
CREATE INDEX idx_equipment_id ON workout (equipment_id);
```

Then i re-run the initial test with explain analyze to check the speed:

### INSERT NEXT SUPABASE PAGE

Conclusion: The added indices improved the speed of the execution time by 1.56ms but the planning time did not change.

The original slowness was due to sequential scans on large tables without targeted indexes, and having to check the foreign key constraints by scanning the workout table. Adding targeted indices allows for direct lookup for rows. 

The index on workout_name allows the database to find rows where workout_name= “workout” in (log) time where before it was sequential.
For the index on muscle_group_id  you can do something similar in addition to joins between workout and muscle_group_id tables being faster. Equipment_id has the same reasons and benefits. 


## 3). For workout_distribution Endpoint:
I run explain analyze on the endpoint in analysis.py:

```
SELECT
    LOWER(muscle_group.muscle_group_name) AS muscle_group,
    ROUND(COUNT(muscle_group.muscle_group_name)::DECIMAL /
        (SELECT COUNT(*)
        FROM user_workout_item
        WHERE user_id = :user_id), 3) AS percentage
FROM user_workout_item
JOIN workout ON user_workout_item.workout_id = workout.workout_id
JOIN muscle_group ON muscle_group.muscle_group_id = workout.muscle_group_id
WHERE user_id = :user_id
GROUP BY muscle_group
```

This command has a planning time of 1.059 ms and an execution time of 5.682 ms. This means that without an index available, it takes the database 5.682 ms to run through all the rows in the table to find the muscle_group_name, yielding the following results: 

('HashAggregate  (cost=53.41..53.91 rows=22 width=64) (actual time=5.558..5.574 rows=17 loops=1)',)
('  Group Key: lower(muscle_group.muscle_group_name)',)
('  Batches: 1  Memory Usage: 24kB',)
('  InitPlan 1 (returns $0)',)
('    ->  Aggregate  (cost=13.09..13.10 rows=1 width=8) (actual time=0.103..0.103 rows=1 loops=1)',)
('          ->  Index Only Scan using idx_user_workout on user_workout_item user_workout_item_1  (cost=0.42..11.92 rows=468 width=0) (actual time=0.028..0.073 rows=471 loops=1)',)
('                Index Cond: (user_id = 400)',)
('                Heap Fetches: 0',)
('  ->  Hash Join  (cost=19.26..37.98 rows=468 width=64) (actual time=4.854..5.339 ros=471 loops=1)',)
('                    Buckets: 1024  Batches: 1  Memory Usage: 27kB',)
('                    ->  Index Only Scan using idx_user_workout on user_workout_item  (cost=0.42..11.92 rows=468 width=8) (actual time=0.050..0.113 rows=471 loops=1)',) 
('                          Index Cond: (user_id = 400)',)
('                          Heap Fetches: 0',)
('        ->  Hash  (cost=1.22..1.22 rows=22 width=40) (actual time=0.020..0.026 rows=22 loops=1)',)
('              Buckets: 1024  Batches: 1  Memory Usage: 10kB',)
('              ->  Seq Scan on muscle_group  (cost=0.00..1.22 rows=22 width=40) (actual time=0.011..0.019 rows=22 loops=1)',)
('Planning Time: 1.059 ms',)
('Execution Time: 5.682 ms',)


I added the following indexes:

```
CREATE INDEX lower_muscle_group_name ON muscle_group (lower(muscle_group_name));
```

After running explain analyze again with the new index and got the following results:

('HashAggregate  (cost=53.41..53.91 rows=22 width=64) (actual time=2.220..2.229 rows=17 loops=1)',)
('  Group Key: lower(muscle_group.muscle_group_name)',)
('  Batches: 1  Memory Usage: 24kB',)
('  InitPlan 1 (returns $0)',)
('    ->  Aggregate  (cost=13.09..13.10 rows=1 width=8) (actual time=0.091..0.092 rows=1 loops=1)',)
('          ->  Index Only Scan using idx_user_workout on user_workout_item user_workout_item_1  (cost=0.42..11.92 rows=468 width=0) (actual time=0.018..0.063 rows=471 loops=1)',)
('                Index Cond: (user_id = 400)',)
('                Heap Fetches: 0',)
('  ->  Hash Join  (cost=19.26..37.98 rows=468 width=64) (actual time=1.554..1.999 ros=471 loops=1)',)
('                    Buckets: 1024  Batches: 1  Memory Usage: 27kB',)
('                    ->  Index Only Scan using idx_user_workout on user_workout_item  (cost=0.42..11.92 rows=468 width=8) (actual time=0.038..0.097 rows=471 loops=1)',) 
('                          Index Cond: (user_id = 400)',)
('                          Heap Fetches: 0',)
('        ->  Hash  (cost=1.22..1.22 rows=22 width=40) (actual time=0.022..0.023 rows=22 loops=1)',)
('              Buckets: 1024  Batches: 1  Memory Usage: 10kB',)
('              ->  Seq Scan on muscle_group  (cost=0.00..1.22 rows=22 width=40) (actual time=0.011..0.014 rows=22 loops=1)',)
('Planning Time: 1.276 ms',)
('Execution Time: 2.343 ms',)


The reason for this change is that previously the database was performing a sequential scan to find the muscle group name, resulting in a longer execution time.
The query now keeps an index of the muscle group names to help quickly find the percent of that muscle group in a user’s workouts.
Using indices allows for a more direct lookup by jumping to the page that contains the data we need. 






