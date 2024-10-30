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
{ "user_id": 1 }
```
2. Get Workouts for Back - /workouts/Weighted_Lunges (GET)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/workouts/Weighted_Lunges' -H 'Content-Type: application/json' 
```
Response:
```json
  { "name": "str", 
  "muscle_groups": ["Back"] },
  ```

3. Add a Workout to the App - /users/{user_id}/workouts (POST)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/workouts' -H 'Content-Type: application/json' -d '{"name":"Weighted Lunges" , muscle_groups:"Legs"}' 
```
Response:
```json
{ "status": "success", 
"message": "Workout added." }
```

4. Add Workouts to User  - /users/{user_id}/workouts (POST)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/users/1/workouts' -H 'Content-Type: application/json' -d '
  "name": "Bench Press",
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


# Example Workflow 3
Example Flow 3: 

Chris introduces his friend Ozcar to the app, and Ozcar is excited to start tracking his workouts with his own personalized data. Ozcar begins by creating an account, calling `POST /users` and providing his name details, which generates a unique user ID for him. Eager to start his fitness journey, Ozcar explores the available workouts by calling `GET /workouts`, which returns a list of exercises along with the muscle groups they target. After browsing through the options, Ozcar decides to start with squats. He calls `POST /users/{user_id}/workouts` to add "Squats" to his workout routine.. With his account set up and his first workout documented, Ozcar is ready to use the app to track his progress and achieve his fitness goals.

  
# Testing Results

1. Add a New User - /users (POST)

Curl Command:
```bash
curl -X 'POST' 'https://csc365-fitness-tracker-1.onrender.com/users' -H 'Content-Type: application/json' -d '{"first_name": "Ozcar", "last_name": "Canete"}'
```
Response:
```json
{ "user_id": 1 }
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

 3. Add Workouts for User - /users/{user_id}/workouts (POST)

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

