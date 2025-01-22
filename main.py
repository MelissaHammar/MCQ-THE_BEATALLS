from user_management import signin_signup
from user_management import load_users,calculate_highest_score, collect_feedback
from mcq_management import load_questions, display_question, export_user_history
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
    question_files = list(category_files.values())

    category_file = None
    while not category_file:
        print("\nPlease select a category:")
        print("1. Artificial Intelligence")
        print("2. Security")
        print("3. Programming")
        print("4. Random (Mixed Categories)")
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
            questions = load_questions(category_file)
        elif category_choice == "4":
            category_name = "Random"
            category_file = "random"  # Placeholder to exit the loop
            # Load questions from all files and combine them
            questions = []
            for file_path in question_files:
                loaded_questions = load_questions(file_path)
                if loaded_questions:
                    questions.extend(loaded_questions)
                else:
                    print(f"Warning: Could not load questions from {file_path}.")
            if not questions:
                print("Error: No questions available for the Random category.")
                category_file = None
        else:
            print("Invalid choice. Please choose correctly.")

    level_map = {'1': "easy", '2': "medium", '3': "hard"}
    # ask the user for the difficulty level
    level_choice = None
    while level_choice not in ['1', '2', '3', '4']:
        print("\nPlease choose a difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Random (Mixed Difficulties)")
        level_choice = input("\nEnter the number for the difficulty level: ")

    # filter questions by level
    if level_choice in {'1', '2', '3'}:
        selected_level = level_map[level_choice]
        filtered_questions = [question for question in questions if question['level'] == selected_level]
    elif level_choice == '4':
        # Include all questions for random difficulty
        filtered_questions = questions
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

    # Randomly select the number of questions
    selected_questions = random.sample(filtered_questions, num_questions)
    total_time = num_questions * 30
    print(f"\nTotal quiz time will be {total_time} seconds ({total_time / 60:.1f} minutes)")
    input("Press Enter when you're ready to start...")

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
        "level": level_map.get(level_choice, "random") if level_choice in level_map else "random",
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

    
    calculate_highest_score(users[user_id]["history"])
    export_user_history(user_id, users[user_id])

    collect_feedback(user_id)




if __name__ == "__main__":
    main()
    