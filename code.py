import json # This format is used on the score and authentication files
import os  # Used to check if a file exists
import random # Used to generate random numbers. But you knew that already. Right?
import time # Used to create delays
from typing import (
    Optional,
)  # Used to create optional function arguments

# Variables
SCORE = 0  # Int
SCORE_TABLE = """
Player  |  Score
--------+---------
{}:      {}
{}:      {}
"""
GREETING_TEXT = """
Welcome to the dice game! The rules are available here:
https://docs.google.com/document/d/1ol2KMvte6Y9FdqIF5vlPE5lkmRVe6RQQXq8v0gjSaLw/edit
To begin, you and a friend (or mortal enemy) will be asked to login to your accounts.
"""

# The user is based on a class object. An example can be seen here: https://www.w3schools.com/python/trypython.asp?filename=demo_class3


class User:
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.highscore = self.get_high_score()

    def add_to_score(self, number) -> None:  # The function doesn't return a value
        self.score += number  # Add the given number to the score.
        if self.score > self.get_high_score():
            self.set_high_score(self.score)
            print(f"{self.name} has a new high score of {self.score}!")

    def subtract_from_score(
        self, number
    ) -> None:  # The function doesn't return a value
        for _ in range(number):
            if self.score != 0:  # The user's score cannot be less than zero
                self.score -= number

    def get_high_score(self) -> int:  # Returns an integer
        file = open(
            f"{self.name}.json", "r"
        )  # The user's highscore is stored in a json file
        json_file = json.load(file)
        score = json_file["highscore"]
        return int(score)

    def set_high_score(
        self, new_score: int
    ) -> None:  # The function doesn't return a value
        original = open(
            f"{self.name}.json", "r"
        ).read()  # The user's highscore is stored in a json file
        json_original = json.loads(original)
        json_original["highscore"] = new_score
        writable_new = open(f"{self.name}.json", "w")
        writable_new.write(
            json.dumps(json_original)
        )  # The new value has been added to the json


def create_user(name: str, password: str):
    try:
        open(f"{name}.json", "x") 
    except FileNotFoundError: # Windows does not allow some file names, for example COM1, and raises a file not found error on trying to create one
        print("Sorry, that is an invalid name for a user. Exiting program...")
    with open(f"{name}.json", "w+", encoding="utf-8") as file:
        file_contents = {"highscore": 0}
        json.dump(file_contents, file)  # Write the above data to the file
    try:
        original = open("users.json", "r").read().replace("\n", "")
    except FileNotFoundError: # The users file does not exist, could happen on first program run
        open("users.json", "x") # Create the file
        original = open("users.json", "r").read().replace("\n", "") # It should exist now
    with open("users.json", "w", encoding="utf-8") as file:
        new_data = {name: password}
        file_json = json.loads(original)
        file_json.update(new_data)
        json.dump(file_json, file)
        file.close()
    return User(name)


def roll_dice():
    dice_roll = random.randint(1, 6)
    print("You rolled: ", str(dice_roll))
    return dice_roll


def get_user_input(text: str, input_type: str):
    user_input = input(text + f" [{input_type}] " + ">>> ")
    return user_input


def total_score(
    **args,
):  # This means that the random numbers generated are stored in a list
    total_score = 0  # Define variable to store the total score in
    for argument in args:  # Loop through every item in the list
        total_score += int(argument)  # Add the value of the item to the total score
    return total_score


def authenticate(username, password):
    valid = False
    authenticated = False
    try:
        users = open("users.json", "r")
    except FileNotFoundError:
        open("users.json", "x") # Create the file, as it doesn't exist yet.
        users = open("users.json", "r")
    users_json = json.load(users)  # Load into a dict object
    if (
        users_json.get(username) is not None
    ):  # The username is in the json, so it is valid
        valid = True
    else:
        print("Sorry, that username is not in our records. Exiting program...")
        exit()
    if users_json[username] == password:
        authenticated = True
    if authenticated == False:
        print("Your password does not match your username. Please try again.")
        return False  # This means an error has occurred.
    elif valid == False:
        print("Sorry, that is not a valid username. Please try again.")
        return False
    elif valid == True and authenticated == True:
        user = User(username)
        print(f"You have successfully logged in as {username}. Your high score is {str(user.get_high_score())}")
        return True
    else:
        print("Sorry, an error occurred whilst logging in.")
        return False  # An error has occurred, so not authenticated. Useful if program is misused.


def authenticate_user(
    player_number: str, player_1: Optional[User] = None
):  # Player 1 is an optional argument used to ensure the same user doesn't log in twice.
    print("Welcome user {}!".format(player_number))
    login_or_create = get_user_input(
        "Would you like to log in or create an account?", "login/create"
    ).lower()
    if login_or_create == "create":
        username_taken = True
        while username_taken == True:
            username = get_user_input(
                "What would you like your username to be?", "text"
            )
            if not os.path.exists("users.json"):
                open("users.json", "x") # Create the file as it does not exist yet.
            if not str(username) in open("users.json", "r").read():
                username_taken = False
            else:
                print(
                    "Sorry, that username is already taken. Please try again with another username."
                )
        password = get_user_input(
            "What would you like your password to be? (Caution - plain text!)", #able to be read in a file 
            "text",
        )
        user = create_user(username, password)
        print("You have successfully created an account!")
        return user
    elif login_or_create == "login":
        while True:
            username = get_user_input("Please enter your username: ", "text")
            password = get_user_input("Please enter your password: ", "text")
            if authenticate(username, password):
                if player_1 is not None:
                    if User(username).name == player_1.name:
                        print("Sorry, you are already logged in. The program will now close in order for you to re-input your information.")
                        print("If this happens, you can always create a new account for your dice game.")
                        exit()
                return User(username)
            else:
                print("Sorry, that didn't match. Please try again.")
    else:
        print("Invalid option. Exiting program...")
        exit()

def leaderboard():
    scores = []
    usernames = []
    leaderboard = json.load(open("users.json", "r"))
    for user in leaderboard.keys():
        user_file = open(f"{user}.json")
        json_user = json.load(user_file)
        scores.append(json_user["highscore"])
        usernames.append(user)
    scores.sort(reverse=True)
    counter = 0
    top_5 = []
    for i in scores:
        top_5.append(i)
        counter += 1
    return usernames, top_5
        

def main():
    print(GREETING_TEXT)
    player_1 = authenticate_user("1")
    player_2 = authenticate_user("2", player_1=player_1)
    round_wins = []
    iteration_counter = 0  # Used to keep track of what round we are on
    while (
        True
    ):  # There are 5 rounds in the game, but if the scores are equal then the loop continues until someone wins.
        iteration_counter += 1
        print("Round {}.".format(iteration_counter))
        player_1_round_total = 0
        player_2_round_total = 0
        for dice_roll in range(1, 3):  # Each player rolls two 6 sided dice
            player_1_roll = roll_dice()
            print(
                f"On their {'first' if dice_roll == 1 else 'second'} go, {player_1.name} rolled: ",
                str(player_1_roll),
            )  # Prints first if the roll is the first one, if not it prints second.
            player_1_round_total += player_1_roll
            if dice_roll == 2 and player_1_round_total % 2 == 0:
                print("Your score was even! Adding 10 points...")
                player_1.add_to_score(10)
            elif dice_roll == 2 and player_1_round_total % 2 != 0:
                print("Your score was odd :( Subtracting 5 from your score...")
                player_1.subtract_from_score(5)
            print("Rolling for player 2...")
            time.sleep(2)
            player_2_roll = roll_dice()
            print(
                f"On their {'first' if dice_roll == 1 else 'second'} go, {player_2.name} rolled: ",
                str(player_1_roll),
            )
            player_2_round_total += player_2_roll
            if dice_roll == 2 and  player_2_round_total % 2 == 0:
                print("Your score was even! :) Adding 10 points...")
                player_2.add_to_score(10)
            elif  dice_roll == 2 and player_2_round_total % 2 != 0:
                print("Your score was odd :( Subtracting 5 from your score...")
                player_1.subtract_from_score(5)
            time.sleep(2)
        print(
            f"__Round total__\n{player_1.name}: {player_1_round_total}\n{player_2.name}: {player_2_round_total}"
        )
        if (
            int(player_1_round_total) == int(player_2_round_total)
            and iteration_counter >= 5
        ):
            print(
                f"{player_1.name} and {player_2.name} have tied. You have an extra round..."
            )
        elif (
            iteration_counter >= 5 and not player_1_round_total == player_2_round_total
        ):
            print(
                f"The game has ended. The winner is {str(player_1.name) if player_1.score > player_2.score else str(player_2.name) } with a score of {str(player_1.score) if player_1.score > player_2.score else str(player_2.score)}!"
            )
            print(SCORE_TABLE.format(player_1.name, str(player_1.score), player_2.name, str(player_2.score)))
            counter  = 0
            print("The overall top scores for this game (in order) are:")
            usernames, top_5 = leaderboard()
            for x in range(0,len(usernames)): # There may not be 5 players yet
                print(str(usernames[x])+ ": "+str(top_5[x]))
            print("Thank you for playing! Press enter to exit...")
            input()
            exit()


if __name__ == "__main__":
    main()
