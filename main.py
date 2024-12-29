from user_management import signin_signup
from user_management import load_users
from mcq_management import load_questions



def main():
    users = load_users()
    #gotta ask the user for the category they want and do an if else statement and change the file path according to that
    questions = load_questions()
    #ask the users about the number of questions 
    user_id = signin_signup(users)

    print("Thank you for playing!")

if __name__ == "__main__":
    main()


