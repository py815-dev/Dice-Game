import json # Used to store scores in a file

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