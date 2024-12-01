### Get Workouts - /workouts/ (GET)

Retrieves a list of workouts that are supported on the fitness app.

Response:

```python
[
  {
    "workout_id": int,
    "workout_name": str,
    "muscle_group_name": str,
    "equipment_name": str
  }
]
```

### Create Custom Workout - /workouts/{workout_name} (POST)

Adds a custom workout to the database.

Parameters:

- workout_name: str
- muscle_group: str
- equipment: str

Response:

```python
{
  "workout_id": int
}
```

### Search Workout - /workouts/search/ (GET)

Finds a workout given filter(s).

Parameters:

- workout_id: int (optional)
- workout_name: str (optional)
- muscle_group_name: str (optional)
- equipment_name: str (optional)

Response:

```python
[
  {
    "workout_id": int,
    "workout_name": str,
    "muscle_group": str,
    "equipment": str
  }
]
```

### Create User - /users/ (POST)

Creates a new user.

Parameters:

- first_name: str
- last_name: str

Response:

```python
{
  "workout_id": int
}
```

### Find User - /users/search/ (GET)

Finds a user given filter(s).

Parameters:

- user_id: int (optional)
- first_name: str (optional)
- last_name: str (optional)

Response:

```python
[
  {
    "user_id": int,
    "first_name": str,
    "last_name": str
  }
]
```

### Update User Workout - /users/{user_id}/workouts/{workout_id} (PUT)

Updates a workout in a user's account.

Parameters:

- user_id: int
- workout_id: int
- sets: int (optional)
- reps: int (optional)
- weight: int (optional)
- rest_time: int (optional)
- one_rep_max: int (optional)

Response:

```python
{
  "message": "Workout updated successfully."
}
```

### Add Workout to User - /users/{user_id}/workouts/{workout_id} (POST)

Adds a workout to a user's profile.

Parameters:

- user_id: int
- workout_id: int
- sets: int
- reps: int
- weight: int
- rest_time: int
- one_rep_max: int

Response:

```python
{
  "message": "Workout added to user successfully."
}
```

### Get User Workouts - /users/{user_id}/workouts (GET)

Retrieves all workouts for a specific user.

Parameters:

- user_id: int
- workout_id: int (optional)

Response:

```python
[
  {
    "workout_id": int,
    "workout_name": str,
    "sets": int,
    "reps": int,
    "weight": int,
    "rest_time": int,
    "one_rep_max": int
  }
]
```

### Delete User Workout - /users/{user_id}/workouts (DELETE)

Deletes a workout from a user's profile.

Parameters:

- user_id: int
- workout_id: int

Response:

```python
{
  "message": "Workout deleted succesfully."
}
```

### Get Workout Tips - /analysis/users/{user_id}/tips/{fitness_goal} (GET)

**Complex Endpoint**

Takes a user's workout routine and analyzes it based on a user's fitness goal. Provides a summary
and then individual analyses on the user's workouts.

Parameters:

- user_id: int
- fitness_goal: str

Response:

```python
{
  "summary": str
  "your_workouts": {
    "workout_name": {
      "sets": str,
      "reps": str,
      "weight": str,
      "rest_time": str
    }
  }
}
```

### Get Workout Distribution - /analysis/users/{user_id}/distributions/ (GET)

**Complex Endpoint**

Analyzes the muscle group distribution of a user's workouts.

Parameters:

- user_id: int

Response:

```python
[
  {
    "muscle_group": float
  }
]
```
