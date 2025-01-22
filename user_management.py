import json
from datetime import datetime

file_users=r"users.json"
# r is used to not treat the \ as a special char

def load_users(file_path= file_users):
    
    try:
        with open(file_path,"r") as file:
            users=json.load(file)
            #de-comment the next line to see that the users are loaded correctly
            #print(f"Loaded {len(users)} users from {file_path}")
            return users
    except FileNotFoundError:
        print(f"Error: File not found, Please check the file path.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the file format.")
        return []


#function to check if it's a sign in or sign up case and do what's needed
def signin_signup(users):
    id = input("Please enter your ID: ").strip()
    if id in users:
        print(f"\nGood to see you again, {id}!")
        print("\nBelow you can find your playing history:") 
        for x in users[id]["history"]:
            print(f"Category: {x['category']}, \t Level: {x['level']}, \t Score: {x['score']}, \t Date: {x['date']}, \t Time: {x['time']}")
        
       
        highest_score = calculate_highest_score(users[id]["history"])
        print(f"\nThe highest number of questions you got right is: {highest_score}")
    # else, sign them up and add their id to the users.json          
    else:
        print(f"\nCreating an account for {id}... ")
        users[id]={"history" : []}
        with open(file_users, "w") as file:
         json.dump(users, file, indent=4) #to update users.json and add the new user     
    return id
    

def calculate_highest_score(history):
    highest = 0
    for entry in history:
        score = int(entry["score"].split('/')[0])  # Extract the numeric score
        if score > highest:
            highest = score
    return highest

def collect_feedback(user_id):
    feedback = input("\nWould you like to provide feedback about the quiz? (yes/no): ").strip().lower()
    if feedback in ['yes', 'y']:
        user_feedback = input("Please enter your feedback: ").strip()
        with open("feedback.txt", "a") as file:
            file.write(f"User {user_id}: {user_feedback}\n")
        print("Thank you for your feedback!\n Goodbye :)" )
    else:
        print("No feedback provided,Thank you for playing! ")
    


