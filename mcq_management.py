import json
import random
from datetime import datetime


#function to load the quetions, with handling 2 exceptions
#when used without arguments it uses the default file path
def load_questions(file_path=r"C:\Users\user\OneDrive\Documents\MY.VSCODES\MCQ-THE_BEATALLS\ai_questions.json"):
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



