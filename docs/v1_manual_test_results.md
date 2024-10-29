# Example workflow
Example Flow 1: 

As a college freshman, Chris is trying to break into weightlifting so he uses our app to track his workouts and receive insights on his progression. First, he creates an account through calling `POST /users/`. He gets a list of the workouts on the app by calling `GET /workouts/` and then adds the workouts he's been trying out by calling `POST /users/{user_id}/workouts/`. After documenting his workouts, he's curious on how to improve his routine, so he calls `GET /analysis/{user_id}/distribution/`. The endpoint reveals that much of his workout is focused on chest exercises, with only 2 workouts targeting his lower-body. Chris adjusts his workouts to get a more balanced distribution and then heads to the gym to attempt his new routine.

  
# Testing results

1. Create a New User - /users (POST)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/users' -H 'Content-Type: application/json' -d '{"first_name": "Chris", "last_name": "Smith"}'
```
Response:
```json
{ "user_id": 1 }
```
2. Get Workouts - /workouts (GET)

Curl Command:
```bash
curl -X 'GET' 'https://csc365-fitness-tracker-1.onrender.com/workouts' -H 'accept: application/json'
```
Response:
```json
  { "name": "Squats", "muscle_groups": ["legs"] },
  ...

3. Add Workouts for User - /users/{user_id}/workouts (POST)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/users/1/workouts' -H 'Content-Type: application/json' -d '{
  "name": "Bench Press",
  "sets": 4,
  "reps": [10, 8, 8, 6],
  "weight": [80, 85, 90, 95],
  "rest_time": [60, 60, 90, 90],
  "one_rep_max_weight": 100
}'
```
Response:
```json
{ "status": "success", "message": "Workout added for user." }
```

4. Get Workout Distribution Analysis - /analysis/{user_id}/distribution (GET)

Curl Command:
```bash
curl -X 'GET' 'https://csc365-fitness-tracker-1.onrender.com/analysis/1/distribution' -H 'accept: application/json'
```
Response:
```json
{
  "result": {
    "chest": 60,
    "back": 20,
    "legs": 20,
    "arms": 0
  }
}

```

