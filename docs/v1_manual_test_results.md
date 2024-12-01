# Example Workflow 1

Example Flow 1:

As a college freshman, Chris is trying to break into weightlifting so he uses our app to track his workouts and receive insights on his progression. First, he creates an account through calling `POST /users/`. He gets a list of the workouts on the app by calling `GET /workouts/` and then adds the workouts he's been trying out by calling `POST /users/{user_id}/workouts/`. After documenting his workouts, he's curious on how to improve his routine, so he calls `GET /analysis/{user_id}/distributions/`. The endpoint reveals that his workout is focused on his forearms only, with no workouts targeting his lower-body. Chris adjusts his workouts to get a more balanced distribution and then heads to the gym to attempt his new routine.

# Testing Results

1. Create a New User - /users/ (POST)

Curl Command:

```bash
curl -X 'POST' \
  'https://csc365-fitness-tracker-1.onrender.com/users/?first_name=Chris&last_name=Test' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker' \
  -d ''
```

Response:

```json
{
  "user_id": 2127
}
```

2. Get Workouts - /workouts/ (GET)

Curl Command:

```bash
curl -X 'GET' \
  'https://csc365-fitness-tracker-1.onrender.com/workouts/' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker'
```

Response:

```json
[
  {
    "workout_id": 93,
    "workout_name": "Zottman Curl",
    "muscle_group_name": "Biceps",
    "equipment_name": "Dumbbells"
  },
  {
    "workout_id": 11,
    "workout_name": "Straight-bar wrist roll-up",
    "muscle_group_name": "Forearms",
    "equipment_name": "Barbell"
  },
  ...
]
```

3. Add Workouts for User - /users/{user_id}/workouts/{workout_id}/ (POST)

Curl Command:

```bash
curl -X 'POST' \
  'https://csc365-fitness-tracker-1.onrender.com/users/2127/workouts/{workout_name}?workout_id=93&sets=3&reps=9&weight=45&rest_time=90&one_rep_max=60' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker' \
  -d ''
```

Response:

```json
{
  "message": "Workout added to user successfully."
}
```

4. Get Workout Distribution Analysis - /analysis/users/{user_id}/distributions/ (GET)

Curl Command:

```bash
curl -X 'GET' \
  'https://csc365-fitness-tracker-1.onrender.com/analysis/users/2127/distributions/' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker'
```

Response:

```json
[
  {
    "biceps": 1
  }
]
```
