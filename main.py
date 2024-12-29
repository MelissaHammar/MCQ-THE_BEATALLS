from user_management import signin_signup
from user_management import load_users
from mcq_management import load_questions, display_question
import random
from datetime import datetime
import json



def main():
    users = load_users()

    print("Welcome to THE BEATALLS MCQ ! \n")

    user_id = signin_signup(users)

    # the user's choice of the category 
    category_files = {
        "1": "ai_questions.json",
        "2": "security_questions.json",
        "3": "programming_questions.json"
    }

    category_file = None
    while not category_file:
        print("\nPlease select a category:")
        print("1. Artificial Intelligence")
        print("2. Security")
        print("3. Programming")
        category_choice = input("\nEnter the number of the category you want to be quized : ")
        
        if category_choice in category_files:
            category_file = category_files[category_choice]

            # save the category name for the history later
            if category_choice == "1":
                category_name = "Artificial Intelligence"
            elif category_choice == "2":
                category_name = "Security"
            elif category_choice == "3":
                category_name = "Programming"
        else:
            print("Invalid choice. Please choose correctly.")

    # loading the questions of the chosen category
    questions = load_questions(category_file)

    # ask the user for the difficulty level
    level_choice = None
    while level_choice not in ['1', '2', '3']:
        print("\nPlease choose a difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        level_choice = input("\nEnter the number for the difficulty level: ")

    # filter questions by level
    level_map = {'1': "easy", '2': "medium", '3': "hard"}
    selected_level = level_map[level_choice]
    filtered_questions = [question for question in questions if question['level'] == selected_level]

    # ask the user about the number of questions 
    while True:
        try:
            num_questions = int(input("\nHow many questions would you like to answer? "))
            if 0 < num_questions <= len(filtered_questions):
                break
            else:
                print(f"Please enter a number between 1 and {len(questions)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    
    total_time = num_questions * 30
    print(f"\nTotal quiz time will be {total_time} seconds ({total_time/60:.1f} minutes)")
    input("Press Enter when you're ready to start...")

    # randomly select the number of questions
    selected_questions = random.sample(filtered_questions, num_questions)

    # initialize the score to 0
    score = 0

    # loop through the questions
    for question_number, question in enumerate(selected_questions, 1):
        if display_question(question, question_number):
            score += 1



    # save the score to the user's history
    now = datetime.now()
    new_score = {
        "category": category_name, 
        "level": selected_level,
        "score": f"{score}/{num_questions}",
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S")
    }

    users[user_id]["history"].append(new_score)

    # update the users.json file
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

    # display final score
    print(f"\nYou completed the quiz! Your final score is {score}/{num_questions}.")


    print("\nThank you for playing!")

if __name__ == "__main__":
    main()


