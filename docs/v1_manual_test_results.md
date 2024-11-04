# Example Workflow 1
Example Flow 1: 

As a college freshman, Chris is trying to break into weightlifting so he uses our app to track his workouts and receive insights on his progression. First, he creates an account through calling `POST /users/`. He gets a list of the workouts on the app by calling `GET /workouts/` and then adds the workouts he's been trying out by calling `POST /users/{user_id}/workouts/`. After documenting his workouts, he's curious on how to improve his routine, so he calls `GET /analysis/{user_id}/distribution/`. The endpoint reveals that his workout is focused on his forearms only, with no workouts targeting his lower-body. Chris adjusts his workouts to get a more balanced distribution and then heads to the gym to attempt his new routine.

  
# Testing Results

1. Create a New User - /users (POST)

Curl Command:
```bash
curl -X 'POST' \
  'https://csc365-fitness-tracker-1.onrender.com/users/Chris/Fix' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker' \
  -d ''
```
Response:
```json
{
  "first_name": "Chris",
  "last_name": "Fix"
}
```
2. Get Workouts - /workouts (GET)

Curl Command:
```bash
curl -X 'GET' \
  'https://csc365-fitness-tracker-1.onrender.com/workouts/' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker'
  ```
Response:
```json
  { 
    "name": "str", 
  "muscle_groups": ["str"] 
  EX:
  
    "name": "Single-Leg Press",
    "muscle_group": "Quadriceps"
  }
  ```

3. Add Workouts for User - /users/{user_id}/workouts (POST)

Curl Command:
```bash
curl -X 'POST' \
  'https://csc365-fitness-tracker-1.onrender.com/users/7/workouts/Palms-up%20wrist%20curl%20over%20bench?sets=2&reps=10&weight=20&rest_time=60&one_rep_max=30' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker' \
  -d ''
```
Response:
```json
{
  "user_id": "7",
  "workout_id": 16,
  "sets": 2,
  "reps": 10,
  "weight": 20,
  "rest_time": 60,
  "one_rep_max": 30
}
```

4. Get Workout Distribution Analysis - /analysis/{user_id}/distribution (GET)

Curl Command:
```bash
curl -X 'POST' \
  'https://csc365-fitness-tracker-1.onrender.com/analysis/7/distribution/' \
  -H 'accept: application/json' \
  -H 'access_token: fitnesstracker' \
  -d ''
  ```
Response:
```json
{
    "Palms-up wrist curl over bench": 1
  }

```


