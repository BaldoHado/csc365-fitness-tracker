# Example Workflow 2
Example Flow 2: 

After using the app for a few weeks, Chris decides to try some new exercises. To see his existing exercises, he starts by calling `GET /workouts/{user_id}`, which returns all the workouts he has saved in his account. While reviewing his progress, he decides to add more back exercises and begins by searching for back workouts, calling `GET /workouts/muscle_groups=back`, which returns a list of recommended exercises targeting the back. Inspired, Chris also decides to create a new custom workout for his lower body. He calls `POST /workouts/Weighted_Lunges` with the details for "Weighted Lunges," specifying that it targets his glutes and quads. With this new exercise saved in his account, Chris adds it to his regular workout routine by calling `POST /users/{user_id}/workouts`, including specific sets, reps, weights, and rest times for the exercise. Now, Chris has expanded his workout plan and is ready to get some new gains so he can be ready for the summer.


# Testing Results

1. Accessing Personal Account Workouts - /workouts/{user_id} (GET)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/workouts/{user_id}' -H 'Content-Type: application/json' 
```
Response:
```json
{ " 'workouts': str[]," }
```

2. Get Workouts for Back - /workouts/search/muscle_groups=back (GET)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/workouts/search/muscle_groups=back' -H 'Content-Type: application/json' 
```
Response:
```json
  { "workout_name": "str" },
  ```

3. Add Weighted Lunges to the App Workouts - /users/{user_id}/workouts (POST)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/workouts' -H 'Content-Type: application/json' -d '{"name":"Weighted Lunges" , muscle_groups:"Legs" equipment:"None"}' 
```
Response:
```json
{ "status": "success", 
"message": "Workout added." }
```

4. Add Weighted Lunges to User Workouts - /users/{user_id}/workouts (POST)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/users/{usre_id}/workouts' -H 'Content-Type: application/json' -d '
  "name": "Weighted Lunges",
  "sets": 2,
  "reps": [10, 8, 10, 10],
  "weight": [30, 30, 25, 20],
  "rest_time": [60, 60, 90, 90],
  "one_rep_max_weight": 70    
```
Response:
```json
{ "status": "success", 
"message": "Workout added for user." }
```


# Example Workflow 3
Example Flow 3: 

  Chris introduces his friend Ozcar to the app, and Ozcar is excited to start tracking his workouts with his own personalized data. Ozcar begins by creating an account, calling `POST /users` to create an account. Eager to start his fitness journey, Ozcar explores the available workouts by calling `GET /workouts`, which returns a list of exercises along with the muscle groups they target. After browsing through the options, Ozcar adds his workouts through `POST /users/{user_id}/workouts`. He's curious on whether his routine is good, so he calls `GET /{user_id}/tips/{fitness_goal}` with his fitness goal being pure strength. The endpoint returns results indicating that he does too many reps per set, and suggests that he increases the weight and lowers the amount of reps. Ozcar alters his routine, optimizing his workouts to build strength.

// add delete user workout
// add change user workout
  
# Testing Results

1. Add a New User - /users (POST)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/users' -H 'Content-Type: application/json' -d '{"first_name": "Ozcar", "last_name": "Canete"}'
```
Response:
```json
{ "user_id": 2 }
``` 
2. Get Workouts from the App - /workouts (GET)

Curl Command:
```bash
curl -X 'GET' 'https://csc365-fitness-tracker-1.onrender.com/workouts' -H 'accept: application/json'
```
Response:
```json
  { "name": "str", 
  "muscle_groups": ["str"] 
  },
  ```

 3. Add Workouts for Oscar - /users/{user_id}/workouts (POST)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/users/1/workouts' -H 'Content-Type: application/json' -d '
  "name": "Squat",
  "sets": 4,
  "reps": [10, 8, 8, 6],
  "weight": [80, 85, 90, 95],
  "rest_time": [60, 60, 90, 90],
  "one_rep_max_weight": 100   
```
Response:
```json
{ "status": "success", 
"message": "Workout added for user." }
```

4. Get User's Fitness Goal - /{user_id}/tips/{fitness_goal} (GET)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/{user_id}/tips/{fitness_goal}' -H 'Content-Type: application/json' 
```
Response:
```json
{
    "sets": {
        "analysis": Literal["low", "just_right", "excessive"],
        "target": int,
      },
    "reps": {
        "analysis": Literal["low", "just_right", "excessive"],
        "target": int,
      },
    "weight": {
        "analysis": Literal["low", "just_right", "excessive"],
        "target": int,
      },
    "rest_time": {
        "analysis": Literal["low", "just_right", "excessive"],
        "target": int,
      }
  }
``` 
