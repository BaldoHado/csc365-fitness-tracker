As a user who is new to fitness, Bob has an idea of what muscles he wants to target but doesn’t know how to. By exploring our API, he can discover exercises for the various muscle groups.

As a user who has some experience in the weight room but has been doing the same workout, Jamal wants to expand his muscle workouts to improve his strength. He inserts his workout routine into our API and explores the workouts in our database to find new workouts. 

As an experienced lifter, Carlos wants to optimize his workouts to the maximum. He wants an even split of the training he does in every muscle group. He calls our API and it gives him a muscle distribution analysis and he alters his workouts accordingly. 

As a new powerlifter, Sally wants to get an analysis on her workout based on her goal of developing pure strength. She inserts her workout routine, weight, sets, reps, and rest time into our app and receives an analysis on how she should change her workouts to maximize her strength goals.

As a person who has trouble staying motivated enough to consistently go to the gym. I want to see that I’m making some kind of progress towards my fitness goals and not feel like I’m wasting my time and money at the gym. 

As a person who doesn’t know much about how to accomplish their fitness goals. I want to be able to figure out where I'm going wrong. So I can accomplish my fitness goals.

As a rising athlete, Charlie wants to train in order to become a professional athlete and wants to keep close track of his workouts and so that he can figure out how he can improve his training regimen.

As a freshman who recently entered college, Chris is new to weightlifting and wants to find ways to optimize his workout with longer breaks or less weight, so that he can maximize his muscle growth. 
As a novice weightlifter, Sean wants to better distribute his workouts to target different muscle groups, so that he develops a more balanced build. 

As a busy college student, Kevin often forgets which workouts he does for each muscle group and wants a way to plan his workouts for the week so that he can make the best use of his limited time at the gym. 

As a professional football player, Leo wants to track his progress and history of the amount of weight he’s able to lift for each of the exercises he does regularly so that he knows if his time at the gym is meeting his goals.

As a high school team coach, Mark wants to find new workouts to give to his athletes that target upper-body. He calls our search endpoint and finds workouts that work chest and shoulders.

As a new athlete who simply wants to gain more stamina and endurance, James explores our API by inserting workouts into his account and calls our /tips/ endpoint with the endurance fitness goal to target his workouts for stamina. 


Exceptions:

- Weight machine / workout isn’t in the database

In the case that the user’s machine or workout isn’t in our database, the application will return back an error and list of similar workouts (e.g. target same muscle group), along with a message to create a custom workout.

- User doesn’t input their full workout

In the case that the user forgets to document a part of their workout (e.g. no breaks in between sets), the user can call an API that inputs the missed activity so that the app will make recommendations based on missing data. 

- User inputs an invalid break time

In this case, the app will return an error indicating that the break time must be a positive integer. 

- User creates a custom workout that already exists

In this case, the app will return the existing workout and alert the user that the workout already exists. If the workout is different, then the user can override the response and the custom workout.

- The app can’t connect to database

In this case, the app will show the user an error message with potential causes and fixes. If the app can’t connect to the internet, it will ask the user to check if they’re connected to the internet.

- User enters an invalid weight

In this case, the app will return an error indicating that the weight must be a positive integer. 

- User enters an invalid set number

In this case, the app will return an error indicating that the set number must be a positive integer. 

- User inserts an invalid user id

In this case, the app will return an error indicating that the user does not exist.

- User adds a workout to their account that already exists

In this case, the app returns a 409 conflict error because the workout already exists.

- User tries to add an invalid workout to their account

In this case, the app returns a 404 not found error to indicate that the workout does not exist.

- User enters invalid reps

In this case, the app will return an error indicating that the reps must be a positive integer. 

- User inserts a very large number for their weight

In this case, the app checks if the value is within the bounds of an 8-bit integer and returns an error if this is not the case.

- User deletes a workout that does not exist in their account

In this case, we return a 404 not found error because the workout is not present in the user's account.
