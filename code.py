import json # Used to store scores in a file
import random # Used to generate random numbers. But you knew that already. Right?

# Variables
SCORE = 0 # Int

# The user is based on a class object. An example can be seen here: https://www.w3schools.com/python/trypython.asp?filename=demo_class3

class User:
    def __init__(name):
        self.name = name
        self.score = 0
        self.highscore = self.get_high_score()
    
    def add_to_score(number):
        self.score += number # Add the given number to the score.
        if self.score > self.get_high_score():
            # TODO write new highscore to file
        
    def subtract_from_score(number):
        for _ in range(number):
            if self.score != 0: # The user's score cannot be less than zero
                self.score -= number
                
    def get_high_score():
        file = open(f"{self.name}.json", "r") # The user's highscore is stored in a json file
        json_file = json.loads(file)
        score = json_file["highscore"]
        return int(score)

def create_user(name:str, password:str):
    open(f"{name}.json", "x")
    with open(f"{name}.json", "w+", encoding='utf-8') as file:
        file_contents = {"highscore": 0}
        json.dump(file_contents, file) # Write the above data to the file
    original = open("users.json", "r").read().replace("\n", "")
    with open("users.json", "w", encoding='utf-8') as file:
        new_data = {name:password}
        file_json = json.loads(file)
        file_json.update(new_data)
        file.close()
    return

def roll_dice():
    dice_roll=random_number
    print(random_number)
    return random_number
def total_score(random_number, random_number2, random_number3, random_number4, random_number5):
    total_score=random_number + random_number2 + random_number3 + random_number4 + random_number5
    return total_score
    
    
def authenticate(username, password):
    valid = False
    authenticated = False
    users = open("users.json")
    users_json = json.loads(users) # Load into a dict object
    if username in users_json.keys:
        valid = True
    if username["password"] == password:
        authenticated = True
    if authenticated == False:
        print("Your password does not match your username. Please try again.")
        return False # This means an error has occurred.
    elif valid == False:
        print("Sorry, that is not a valid username. Please try again.")
        return False
    elif valid == True and authenticated == True:
        print("You have successfully logged in.")
        return True
    else:
        print("Sorry, an error occurred whilst logging in.")
        return False # An error has occurred, so not authenticated. Useful if program is misused.
