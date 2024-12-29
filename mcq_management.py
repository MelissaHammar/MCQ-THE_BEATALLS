import json
import random
from datetime import datetime


#function to load the quetions, with handling 2 exceptions
#when used without arguments it uses the default file path
def load_questions(file_path):
    try:
        with open(file_path,"r") as file:
            questions=json.load(file)
            #de-comment the next line to see that the questions are loaded correctly
            #print(f"Loaded {len(questions)} questions from {file_path}")
            return questions
    except FileNotFoundError:
        print(f"Error: File not found, Please check the file path.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the file format.")
        return []


# function to display a question and handle user answer
def display_question(question, question_number):
    print(f"\nQuestion {question_number}: {question['question']}")
    for idx, option in enumerate(question['options'], 1):
        print(f"{idx}. {option}")

    # get and validate user input
    while True:
        try:
            user_answer = int(input("Your answer (enter the number): "))
            if 1 <= user_answer <= len(question['options']):
                break
            else:
                print("Please enter a valid option number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # check if the answer is correct
    if user_answer == question['answer']:
        print("Correct!")
        return True
    else:
        correct_option = question['options'][question['answer'] - 1]
        print(f"Wrong! The correct answer was: {correct_option}")
        return False

