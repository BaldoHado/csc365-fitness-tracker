# Example Workflow 2

Example Flow 2:

After using the app for a few weeks, Chris decides to try some new exercises. To see his existing exercises, he starts by calling `GET /users/{user_id}/workouts/`, which returns all the workouts he has saved in his account. While reviewing his progress, he decides to add more back exercises and begins by searching for lower back workouts, calling `GET /workouts/search/?muscle_group_name=back/`, which returns a list of recommended exercises targeting the lower back. Inspired, Chris also decides to create a new custom workout for his lower body. He calls `POST /workouts/{workout_name}/` with the details for "Weighted Lunges," specifying that it targets his hamstrings, and uses dumbbells. With this new exercise saved in his account, Chris adds it to his regular workout routine by calling `POST /users/{user_id}/workouts/`, including specific sets, reps, weights, and rest times for the exercise. Now, Chris has expanded his workout plan and is ready to get some new gains so he can be ready for the summer.

# Testing Results

1. Accessing Personal Account Workouts - /users/{user_id}/workouts/ (GET)

Curl Command:

```bash
curl -X 'GET' \
  'https://csc365-fitness-tracker-1.onrender.com/users/2127/workouts' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker'
```

Response:

```json
[
  {
    "workout_id": 93,
    "workout_name": "Zottman Curl",
    "sets": 3,
    "reps": 9,
    "weight": 45,
    "rest_time": 90,
    "one_rep_max": 60
  },
  {
    "workout_id": 313,
    "workout_name": "Alternate Hammer Curl",
    "sets": 4,
    "reps": 5,
    "weight": 45,
    "rest_time": 120,
    "one_rep_max": 65
  }
]
```

2. Get Workouts for Lower Back - /workouts/search/ (GET)

Curl Command:

```bash
curl -X 'GET' \
  'https://csc365-fitness-tracker-1.onrender.com/workouts/search/?muscle_group_name=lower%20back' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker'
```

Response:

```json
[
  {
    "workout_id": 18,
    "workout_name": "Barbell deficit deadlift",
    "muscle_group": "Lower Back",
    "equipment": "Barbell"
  },
  {
    "workout_id": 65,
    "workout_name": "Back extension",
    "muscle_group": "Lower Back",
    "equipment": "Body Only"
  },
  {
    "workout_id": 80,
    "workout_name": "Back extension",
    "muscle_group": "Lower Back",
    "equipment": "Body Only"
  },
  {
    "workout_id": 92,
    "workout_name": "Axle Deadlift",
    "muscle_group": "Lower Back",
    "equipment": "Other"
  },
  {
    "workout_id": 247,
    "workout_name": "Hyperextensions With No Hyperextension Bench",
    "muscle_group": "Lower Back",
    "equipment": "Body Only"
  },
  {
    "workout_id": 295,
    "workout_name": "Deadlift with Bands",
    "muscle_group": "Lower Back",
    "equipment": "Barbell"
  },
  {
    "workout_id": 322,
    "workout_name": "Deadlift with Chains",
    "muscle_group": "Lower Back",
    "equipment": "Barbell"
  },
  {
    "workout_id": 368,
    "workout_name": "Rack Pull with Bands",
    "muscle_group": "Lower Back",
    "equipment": "Barbell"
  },
  {
    "workout_id": 374,
    "workout_name": "Rack Pull with Bands",
    "muscle_group": "Lower Back",
    "equipment": "Barbell"
  },
  {
    "workout_id": 7,
    "workout_name": "Atlas Stones",
    "muscle_group": "Lower Back",
    "equipment": "Other"
  },
  {
    "workout_id": 448,
    "workout_name": "Superman",
    "muscle_group": "Lower Back",
    "equipment": "Body Only"
  },
  {
    "workout_id": 485,
    "workout_name": "Tree Climbs",
    "muscle_group": "Lower Back",
    "equipment": "Bodyweight"
  },
  {
    "workout_id": 488,
    "workout_name": "Tree Climbers",
    "muscle_group": "Lower Back",
    "equipment": "Bodyweight"
  }
]
```

3. Create Weighted Lunges as a Custom Workout - /workouts/{workout_name}/ (POST)

Curl Command:

```bash
curl -X 'POST' \
  'https://csc365-fitness-tracker-1.onrender.com/workouts/weighted%20lunges?muscle_group=hamstrings&equipment=dumbbell' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker' \
  -d ''
```

Response:

```json
{
  "workout_id": 483
}
```

4. Add Weighted Lunges to User Workouts - /users/{user_id}/workouts/ (POST)

Curl Command:

```bash
curl -X 'POST' \
  'https://csc365-fitness-tracker-1.onrender.com/users/2127/workouts/483?sets=2&reps=10&weight=35&rest_time=60&one_rep_max=80' \
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

# Example Workflow 3

Example Flow 3:

Chris introduces his friend Ozcar to the app, and Ozcar is excited to start tracking his workouts with his own personalized data. Ozcar begins by creating an account, calling `POST /users/` to create an account. Eager to start his fitness journey, Ozcar explores the available workouts by calling `GET /workouts/`, which returns a list of exercises along with the muscle groups they target. After browsing through the options, Ozcar adds his workouts through `POST /users/{user_id}/workouts/{workout_id}/`. He's curious on whether his routine is good, so he calls `GET /analysis/users/{user_id}/tips/{fitness_goal}/` with his fitness goal being pure strength. The endpoint returns results indicating that he does too many reps per set, and suggests that he increases the weight and lowers the amount of reps. Ozcar alters his routine, optimizing his workouts to build strength.

# Testing Results

1. Add a New User - /users/ (POST)

Curl Command:

```bash
curl -X 'POST' \
  'https://csc365-fitness-tracker-1.onrender.com/users/?first_name=Ozcar&last_name=Canete' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker' \
  -d ''
```

Response:

```json
{
  "user_id": 2128
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

3. Add Workouts for Oscar - /users/{user_id}/workouts/{workout_id}/ (POST)

Curl Command:

```bash
curl -X 'POST' \
  'https://csc365-fitness-tracker-1.onrender.com/users/2128/workouts/316?sets=4&reps=10&weight=60&rest_time=60&one_rep_max=120' \
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

4. Get Analysis Based On Strength Fitness Goal - /analysis/users/{user_id}/tips/{fitness_goal}/ (GET)

Curl Command:

```bash
curl -X 'GET' \
  'https://csc365-fitness-tracker-1.onrender.com/analysis/users/2128/tips/strength' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker'
```

Response:

```json
{
  "summary": "When training for strength, focus on lifting as heavy as you can safely manage for a few powerful reps. Take longer rest periods to fully recover between sets and maintain maximum effort. Prioritize progressive overload and proper form to steadily build strength.",
  "your_workouts": {
    "Triceps Pushdown": {
      "sets": "just_right",
      "reps": "too_much",
      "weight": "too_low",
      "rest_time": "too_low"
    }
  }
}
```
