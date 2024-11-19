### Get Workouts - /workouts/ (GET)
Retrieves a list of workouts that are supported on the fitness app.

Response:
```python
[
  {
    "name": str,
    "muscle_group": str
  }
]
```

### Get Workouts by Muscle Group - /workouts/{muscle_group} (GET)
Retrieves workouts filtered by muscle group.

Parameters:
- muscle_group: str (path parameter)

Response:
```python
[
  {
    "name": str,
    "muscle_group": str
  }
]
```

### Search Workout - /workouts/search/{workout_name} (GET)
Searches for a specific workout by name.

Parameters:
- workout_name: str (path parameter)

Response:
```python
{
  "workout_id": int,
  "workout_name": str,
  "muscle_group": str,
  "equipment": str
}
```

### Create Custom Workout - /workouts/workouts/{workout_name}/{muscle_group}/{equipment} (POST)
Creates a new custom workout.

Parameters:
- workout_name: str (path parameter)
- muscle_group: str (path parameter)
- equipment: str (path parameter)

Response:
```python
[
  {
    "name": str,
    "muscle_group": str,
    "equipment": str
  }
]
```

### Create User - /users/{first_name}/{last_name} (POST)
Creates a new user.

Parameters:
- first_name: str (path parameter)
- last_name: str (path parameter)

Response:
```python
{
  "first_name": str,
  "last_name": str
}
```

### Get User Workouts - /users/{user_id}/workouts (GET)
Retrieves all workouts for a specific user.

Parameters:
- user_id: str (path parameter)

Response:
```python
[
  {
    "workout_name": str,
    "sets": int,
    "reps": int,
    "weight": int,
    "rest_time": int,
    "one_rep_max": int
  }
]
```

### Add Workout to User - /users/{user_id}/workouts/{workout_name} (POST)
Adds a workout to a user's profile.

Parameters:
- user_id: str (path parameter)
- workout_name: str (path parameter)
- sets: int
- reps: int
- weight: int
- rest_time: int
- one_rep_max: int

Response:
```python
{
  "user_id": str,
  "workout_id": int,
  "sets": int,
  "reps": int,
  "weight": int,
  "rest_time": int,
  "one_rep_max": int
}
```

### Update User Workout - /users/{user_id}/workouts/{workout_name} (PUT)
Updates a user's workout details.

Parameters:
- user_id: str (path parameter)
- workout_name: str (path parameter)
- sets: int (optional)
- reps: int (optional)
- weight: int (optional)
- rest_time: int (optional)
- one_rep_max: int (optional)

Response:
```python
"OK"
```

### Delete User Workout - /users/{user_id}/workouts (DELETE)
Deletes a workout from a user's profile.

Parameters:
- user_id: str (path parameter)
- workout_name: str

Response:
```python
"OK"
```

### Get Workout Tips - /analysis/{user_id}/tips/{fitness_goal} (GET)
This is a Complex Endpoint that retrieves workout tips based on user's fitness goal.
It analyzes detailed user workout data against fitness goals using advanced logic and helper functions. It also handles edge cases where no data is there. 

Parameters:
- user_id: str (path parameter)
- fitness_goal: str (path parameter)

Response:
```python
{
  "workout_name": {
    "sets": str,
    "reps": str,
    "weight": str,
    "rest_time": str
  }
}
```

### Get Workout Distribution - /analysis/{user_id}/distribution/ (POST)
This is a complex endpoint that analyzes the distribution of workouts for a user.
It calculates and aggregates workout distribution percentages across muscle groups using SQL joins and other functions. It also handles edge cases where no data is there. 

Parameters:
- user_id: str (path parameter)

Response:
```python
[
  {
    "workout_name": float
  }
]
```