import json
import random
from datetime import datetime
import time
from threading import Timer


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
from threading import Timer

def display_question(question, question_number):
    # Print the question
    print(f"\nQuestion {question_number}: {question['question']}")
    for idx, option in enumerate(question['options'], 1):
        print(f"{idx}. {option}")
    
    # Initialize variables
    user_answer = None
    timer_expired = False
    
    def on_timeout():
        nonlocal timer_expired
        timer_expired = True
        print(f"\nTime's up! The correct answer was: {question['options'][question['answer'] - 1]}")  # Updated message
        print("Press Enter to continue... ")
    
    # Start the timer
    timer = Timer(30.0, on_timeout)
    timer.start()
    
    # Get user input while timer hasn't expired
    while not timer_expired:
        try:
            user_input = input("\nYour answer (enter the number): ").strip()
            if user_input == "" and timer_expired:  # Handle Enter key after timeout
                break
            user_answer = int(user_input)
            if 1 <= user_answer <= len(question['options']):
                break
            else:
                print("Please enter a valid option number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except EOFError:  # Handle Ctrl+D
            break
    
    # Cancel timer if answer was given
    timer.cancel()
    
    # If timer expired or no valid answer, return False
    if timer_expired or user_answer is None:
        return False
        
    # Check if answer is correct
    if user_answer == question['answer']:
        print("Correct!")
        return True
    else:
        correct_option = question['options'][question['answer'] - 1]
        print(f"Wrong! The correct answer was: {correct_option}")
        return False
    
#function to export the user's data if needed
def export_user_history(user_id, user_data):
    """
    Export the user's history to a text file.
    """
    export_choice = input("\nDo you want to export your history to a file? (yes/no): ").strip().lower()
    
    if export_choice == 'yes':
        filename = f"{user_id}_history.txt"
        
        try:
            with open(filename, "w") as file:
                file.write(f"User ID: {user_id}\n")
                file.write("Playing History:\n")
                file.write("-" * 30 + "\n")
                
                # Check if user has history
                history = user_data.get("history", [])
                if not history:
                    file.write("No history available.\n")
                else:
                    for entry in history:
                        file.write(
                            f"Category: {entry.get('category', 'N/A')}\n"
                            f"Level: {entry.get('level', 'N/A')}\n"
                            f"Score: {entry.get('score', 'N/A')}\n"
                            f"Date: {entry.get('date', 'N/A')}\n"
                            f"Time: {entry.get('time', 'N/A')}\n"
                            f"{'-' * 30}\n"
                        )
            print(f"\nHistory successfully exported to {filename}")
        except Exception as e:
            print(f"An error occurred while exporting history: {e}")
    else:
        print("\nExport canceled.")
