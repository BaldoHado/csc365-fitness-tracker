Example Flow 1: 

As a college freshman, Chris is trying to break into weightlifting so he uses our app to track his workouts and receive insights on his progression. First, he creates an account through calling `POST /users/`. He gets a list of the workouts on the app by calling `GET /workouts/` and then adds the workouts he's been trying out by calling `POST /users/{user_id}/workouts/`. After documenting his workouts, he's curious on how to improve his routine, so he calls `GET /analysis/{user_id}/distribution/`. The endpoint reveals that much of his workout is focused on chest exercises, with only 2 workouts targeting his lower-body. Chris adjusts his workouts to get a more balanced distribution and then heads to the gym to attempt his new routine.

Example Flow 2: Adding Exercises

After using the app for a few weeks, Chris decides to try some new exercises. To see his existing exercises, he starts by calling `GET /workouts/{user_id}`, which returns all the workouts he has saved in his account. While reviewing his progress, he decides to add more back exercises and begins by searching for back workouts, calling `GET /workouts/muscle_groups=back`, which returns a list of recommended exercises targeting the back. Inspired, Chris also decides to create a new custom workout for his lower body. He calls `POST /workouts/Weighted_Lunges` with the details for "Weighted Lunges," specifying that it targets his glutes and quads. With this new exercise saved in his account, Chris adds it to his regular workout routine by calling `POST /users/{user_id}/workouts`, including specific sets, reps, weights, and rest times for the exercise. Now, Chris has expanded his workout plan and is ready to get some new gains so he can be ready for the summer.

Example Flow 3: Adding a new User

Chris introduces his friend Ozcar to the app, and Ozcar is excited to start tracking his workouts with his own personalized data. Ozcar begins by creating an account, calling `POST /users` and providing his name details, which generates a unique user ID for him. Eager to start his fitness journey, Ozcar explores the available workouts by calling `GET /workouts`, which returns a list of exercises along with the muscle groups they target. After browsing through the options, Ozcar decides to start with squats. He calls `POST /users/{user_id}/workouts` to add "Squats" to his workout routine.. With his account set up and his first workout documented, Ozcar is ready to use the app to track his progress and achieve his fitness goals.


