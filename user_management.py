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
    id=input("Please enter your ID : ").strip()
   # if the user exists then print their history
    if id in users:
        print(f"\nGood to see you again, {id}!")
        print(f"\nBelow you can find your playing history: ") 
        for x in users[id]["history"] : 
            print(f"Category: {x['category']}, \t Level: {x['level']}, \t Score: {x['score']}, \t Date: {x['date']}, \t Time: {x['time']}")
    # else, sign them up and add their id to the users.json          
    else:
        print(f"\nCreating an account for {id}... ")
        users[id]={"history" : []}
        with open(file_users, "w") as file:
         json.dump(users, file, indent=4) #to update users.json and add the new user     
    return id
    

    


