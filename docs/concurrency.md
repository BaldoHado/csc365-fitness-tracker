### Write Skew

T1 calls on /workouts/{workout_name}/{muscle_group}/{equipment} and performs a select query to check if the workout exists in the database

T2 calls on the same endpoint and also performs a select to check if their workout name already exists

Both queries result in the data not existing so two rows are inserted into the database with the same data

One potential solution is to use the FOR UPDATE keyword in sql which locks rows from being accessed until the lock is released

### Lost Update

T1 calls PUT  /{user_id}/workouts/{workout_id} to update a workout in their account.

T2 calls PUT  /{user_id}/workouts/{workout_id} to update the same workout in the same account.

The queries conflict, and one query overrides the other’s changes, resulting in a lost update.

The solution is to use the serializable isolation level, as it ensures that transactions executed concurrently will have the same result as if they were processed separately. 


### Dirty Read

T1 calls PUT /users/{user_id}/workouts/{workout_id} to update the sets for a workout and writes the uncommitted change to the database.

T2 calls GET /users/{user_id}/workouts and retrieves the workout information, including the uncommitted change made by T1.

T1 encounters an error and rolls back the transaction.

T2 has already used the new, invalid data, causing inconsistencies. 

The Solution is to use the Read Committed isolation level to ensure that T2 can only access the committed data. One way to do this is to use the sql: SET transaction isolation level read committed;
