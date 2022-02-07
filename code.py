from ast import While
import json
import os  # Used to store scores in a file
import random
import time
from typing import (
    Optional,
)  # Used to generate random numbers. But you knew that already. Right?

# Variables
SCORE = 0  # Int
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
    open(f"{name}.json", "x")
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
        print(f"You have successfully logged inas {username}. Your high score is 0")
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
    )
    if login_or_create == "create":
        username_taken = True
        while username_taken == True:
            username = get_user_input(
                "What would you like your username to be?", "text"
            )
            if not str(username) in open("users.json", "r").read():
                username_taken = False
            else:
                print(
                    "Sorry, that username is already taken. Please try again with another username."
                )
        password = get_user_input(
            "What would you like your password to be? (Caution - plain text!)",
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
                if User(username) == player_1:
                    print("Sorry, you are already logged in.")
                else:
                    return User(username)
            else:
                print("Sorry, that didn't match. Please try again.")
    else:
        print("Invalid option. Exiting program...")


def main():
    print(GREETING_TEXT)
    player_1 = authenticate_user("1")
    player_2 = authenticate_user("2", player_1=player_1)
    iteration_counter = 0  # Used to keep track of what round we are on
    while (
        True
    ):  # There are 5 rounds in the game, but if the scores are equal then the loop continues until someone wins.
        iteration_counter += 1
        print("Round {}.".format(iteration_counter))
        player_1_round_total = 0
        player_2_round_total = 0
        for dice_roll in range(1, 2):  # Each player rolls two 6 sided dice
            player_1_roll = roll_dice()
            print(
                f"On their {'first' if dice_roll == 1 else 'second'} go, {player_1.name} rolled: ",
                str(player_1_roll),
            )  # Prints first if the roll is the first one, if not it prints second.
            player_1_round_total += player_1_roll
            player_1.add_to_score(player_1_roll)
            print("Rolling for player 2...")
            time.sleep(2)
            player_2_roll = roll_dice()
            print(
                f"On their {'first' if dice_roll == 1 else 'second'} go, {player_2.name} rolled: ",
                str(player_1_roll),
            )
            player_2_round_total += player_2_roll
            player_2.add_to_score(player_2_roll)
            time.sleep(2)
        print(
            f"Round total:\n{player_1.name}: {player_1_round_total}\n{player_2.name}: {player_2_round_total}"
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
            print("Thank you for playing!")
            exit()


if __name__ == "__main__":
    main()
