from flask import Flask
from flask import request
import json
import webbrowser as wb

wb.open("http://localhost")

app = Flask(__name__)

SCORE = 0  # Int
SCORE_TABLE = """
Player     |  Score
-----------+---------
{}:      {}
{}:      {}
"""
GREETING_TEXT = """
Welcome to the dice game! The rules are available here:
https://docs.google.com/document/d/1ol2KMvte6Y9FdqIF5vlPE5lkmRVe6RQQXq8v0gjSaLw/edit
To begin, you and a friend (or mortal enemy) will be asked to login to your accounts.
"""

player_2 = 0

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

# The user is based on a class object. An example can be seen here: https://www.w3schools.com/python/trypython.asp?filename=demo_class3

def authenticate_user(player_number:str="1", player_1: User=None, username:str="me", password:str="myself"):  # Player 1 is an optional argument used to ensure the same user doesn't log in twice.
    login_or_create = "login"
    if login_or_create == "login":
        while True:
            if authenticate(username, password):
                if player_1 is not None:
                    if User(username).name == player_1.name:
                        return False, "Already logged in."
                return True, User(username)
            else:
                return False, "Sorry, that didn't match. Please try again."
    else:
        print("Invalid option. Exiting program...")
        exit()


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
    return dice_roll

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
        return False, "Sorry, that username is not in our records."
    if users_json[username] == password:
        authenticated = True
    if authenticated == False:
        return False, "Your password does not match your username. Please try again."  # This means an error has occurred.
    elif valid == False:
        return False, "Sorry, that is not a valid username. Please try again."
    elif valid == True and authenticated == True:
        user = User(username)
        return True, f"You have successfully logged in as {username}. Your high score is {str(user.get_high_score())}"
    else:
        return False, "Sorry, an error occurred whilst logging in."  # An error has occurred, so not authenticated. Useful if program is misused.

@app.route("/")
def hello():
    return """
<!DOCTYPE html>
<html>
<title>Dice Game</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<body>

<div class="w3-container">
  <h2>User 1 login</h2>

  <button onclick="document.getElementById('id01').style.display='block'" class="w3-button w3-blue w3-large">Login</button>

  <div id="id01" class="w3-modal">
    <div class="w3-modal-content w3-card-4 w3-animate-zoom" style="max-width:600px">
  
      <div class="w3-center"><br>
        <span onclick="document.getElementById('id01').style.display='none'" class="w3-button w3-xlarge w3-transparent w3-display-topright" title="Close Modal">×</span>
        <img src="https://media.istockphoto.com/vectors/pair-of-dice-to-stake-or-gambling-with-craps-line-art-vector-icon-for-vector-id1212735107?k=20&m=1212735107&s=612x612&w=0&h=7GL0qbC9cX5UWAGWasLKBZ41_Sc-jpDWr9g6l6Ir9SI=" alt="Avatar" style="width:30%" class="w3-circle w3-margin-top">
      </div>

      <form class="w3-container" action="/login2">
        <div class="w3-section">
          <label><b>Username</b></label>
          <input class="w3-input w3-border w3-margin-bottom" type="text" placeholder="Enter Username" name="usrname" required>
          <label><b>Password</b></label>
          <input class="w3-input w3-border" type="text" placeholder="Enter Password" name="psw" required>
          <button class="w3-button w3-block w3-blue w3-section w3-padding" type="submit">Login</button>
        </div>
      </form>

      <div class="w3-container w3-border-top w3-padding-16 w3-light-grey">
        <button onclick="document.getElementById('id01').style.display='none'" type="button" class="w3-button w3-red">Cancel</button>
      </div>

    </div>
  </div>
</div>
            
</body>
</html>
"""
player_1 = ""
@app.route("/login2", methods=["GET"])
def login2():
    global player_1
    username = request.args.get('usrname')
    password = request.args.get('psw')
    worked, message = authenticate(username, password)
    _, player_1 = authenticate_user("1", None, username, password)
    return """
<!DOCTYPE html>
<html>
<title>Dice Game</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<body>
<script>
alert('{}');
</script>
<div class="w3-container">
  <h2>User 2 login</h2>

  <button onclick="document.getElementById('id01').style.display='block'" class="w3-button w3-blue w3-large">Login</button>

  <div id="id01" class="w3-modal">
    <div class="w3-modal-content w3-card-4 w3-animate-zoom" style="max-width:600px">
  
      <div class="w3-center"><br>
        <span onclick="document.getElementById('id01').style.display='none'" class="w3-button w3-xlarge w3-transparent w3-display-topright" title="Close Modal">×</span>
        <img src="https://media.istockphoto.com/vectors/pair-of-dice-to-stake-or-gambling-with-craps-line-art-vector-icon-for-vector-id1212735107?k=20&m=1212735107&s=612x612&w=0&h=7GL0qbC9cX5UWAGWasLKBZ41_Sc-jpDWr9g6l6Ir9SI=" alt="Avatar" style="width:30%" class="w3-circle w3-margin-top">
      </div>

      <form class="w3-container" action="/game">
        <div class="w3-section">
          <label><b>Username</b></label>
          <input class="w3-input w3-border w3-margin-bottom" type="text" placeholder="Enter Username" name="usrname" required>
          <label><b>Password</b></label>
          <input class="w3-input w3-border" type="text" placeholder="Enter Password" name="psw" required>
          <button class="w3-button w3-block w3-blue w3-section w3-padding" type="submit">Login</button>
        </div>
      </form>

      <div class="w3-container w3-border-top w3-padding-16 w3-light-grey">
        <button onclick="document.getElementById('id01').style.display='none'" type="button" class="w3-button w3-red">Cancel</button>
      </div>

    </div>
  </div>
</div>
            
</body>
</html>
""".format(message)

round_number = 0

@app.route("/game", methods=["GET"])
def game():
    global player_2
    global round_number
    round_number += 1
    username = request.args.get('usrname')
    password = request.args.get('psw')
    worked, messageorusr = authenticate_user("2", None, username, password)
    if worked == True:
        player_2 = messageorusr
        return """
<!DOCTYPE html>
<html>
<title>Dice Game</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-blue.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<body>

<div class="w3-sidebar w3-collapse w3-white w3-animate-left w3-large" style="z-index:3;width:300px;" id="mySidebar">


<div id="nav01" class="w3-bar-block">
  <a class="w3-button w3-hover-blue w3-hide-large w3-large w3-right" href="javascript:void(0)" onclick="w3_close()">×</a>
  <a class="w3-bar-item w3-button" href="#"></a>
  <a class="w3-bar-item w3-button" href="#"></a>
</div>


<div id="nav03">
  <div class="w3-container w3-border-bottom">
    <h1 class="w3-text-theme">Dice Game</h1>
    <h2>"""+messageorusr.name+""" - """+str(messageorusr.score)+"""</h2>
    <h2>"""+player_1.name+""" - """+str(player_1.score)+"""</h2>
  </div>
</div>
</div>

<div class="w3-overlay w3-hide-large" onclick="w3_close()" style="cursor:pointer" id="myOverlay"></div>

<div class="w3-main" style="margin-left:300px;"> 

<div class="w3-top w3-blue w3-large w3-hide-large">
  <i class="fa fa-bars w3-button w3-blue w3-xlarge" onclick="w3_open()"></i>
</div>

<header class="w3-container w3-blue w3-padding-64 w3-center">
  <h1 class="w3-xxxlarge w3-padding-16">Dice Game</h1>
</header>

<div class="w3-container w3-padding-large w3-section w3-light-grey">
  <h1 class="w3-jumbo">"""+f"Round {str(round_number)} total"+"""</h1>
  <p class="w3-xlarge">Click to roll</p>
  <form class="w3-container" action="/roll/">
  <button class="w3-button w3-block w3-blue w3-section w3-padding" type="submit">Roll</button>
  </form>

</div>


<footer class="w3-container w3-padding-large w3-light-grey w3-justify w3-opacity">
  <h3>Made by Team Toad</h3>
</footer>

</div>

<script>
function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
}

function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}

openNav("nav01");
function openNav(id) {
  document.getElementById("nav01").style.display = "none";
  document.getElementById("nav02").style.display = "none";
  document.getElementById("nav03").style.display = "none";
  document.getElementById(id).style.display = "block";
}
</script>

<script src="https://www.w3schools.com/lib/w3codecolor.js"></script>

<script>
w3CodeColor();
</script>

</body>
</html> 
"""
    else:
        return messageorusr

import random
round_number = 0
@app.route("/roll/")
def roll():
    global player_1
    global player_2
    global round_number
    round_number += 1
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
        player_2_roll = roll_dice()
        print(
                f"On their {'first' if dice_roll == 1 else 'second'} go, {player_2.name} rolled: ",
                str(player_1_roll),
        )
        player_2_round_total += player_2_roll
        if dice_roll == 2 and  player_2_round_total % 2 == 0:
            print("Your score was even! Adding 10 points...")
            player_2.add_to_score(10)
        elif  dice_roll == 2 and player_2_round_total % 2 != 0:
            print("Your score was odd :( Subtracting 5 from your score...")
            player_1.subtract_from_score(5)
    if round_number == 5:
        return """
<!DOCTYPE html>
<html>
<title>Dice Game</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-blue.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<body>

<div class="w3-sidebar w3-collapse w3-white w3-animate-left w3-large" style="z-index:3;width:300px;" id="mySidebar">


<div id="nav01" class="w3-bar-block">
  <a class="w3-button w3-hover-blue w3-hide-large w3-large w3-right" href="javascript:void(0)" onclick="w3_close()">x</a>
  <a class="w3-bar-item w3-button" href="#"></a>
  <a class="w3-bar-item w3-button" href="#"></a>
</div>


<div id="nav03">
  <div class="w3-container w3-border-bottom">
    <h1 class="w3-text-theme">"""+f"Round {str(round_number)} Score"+"""</h1>
    <h2>"""+player_2.name+""" - """+str(player_2.score)+"""</h2>
    <h2>"""+player_1.name+""" - """+str(player_1.score)+"""</h2>
  </div>
</div>
</div>

<div class="w3-overlay w3-hide-large" onclick="w3_close()" style="cursor:pointer" id="myOverlay"></div>

<div class="w3-main" style="margin-left:300px;"> 

<div class="w3-top w3-blue w3-large w3-hide-large">
  <i class="fa fa-bars w3-button w3-blue w3-xlarge" onclick="w3_open()"></i>
</div>

<header class="w3-container w3-blue w3-padding-64 w3-center">
  <h1 class="w3-xxxlarge w3-padding-16">Dice Game</h1>
</header>

<div class="w3-container w3-padding-large w3-section w3-light-grey">
  <h1 class="w3-jumbo">Game Over!</h1>
  <p class="w3-xlarge">Thanks for playing!</p>

</div>


<footer class="w3-container w3-padding-large w3-light-grey w3-justify w3-opacity">
  <h3>Made by Team Toad</h3>
</footer>

</div>

<script>
function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
}

function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}

openNav("nav01");
function openNav(id) {
  document.getElementById("nav01").style.display = "none";
  document.getElementById("nav02").style.display = "none";
  document.getElementById("nav03").style.display = "none";
  document.getElementById(id).style.display = "block";
}
</script>

<script src="https://www.w3schools.com/lib/w3codecolor.js"></script>

<script>
w3CodeColor();
</script>

</body>
</html>
"""
    else:
        return """
<!DOCTYPE html>
<html>
<title>Dice Game</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-blue.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<body>

<div class="w3-sidebar w3-collapse w3-white w3-animate-left w3-large" style="z-index:3;width:300px;" id="mySidebar">


<div id="nav01" class="w3-bar-block">
  <a class="w3-button w3-hover-blue w3-hide-large w3-large w3-right" href="javascript:void(0)" onclick="w3_close()">×</a>
  <a class="w3-bar-item w3-button" href="#"></a>
  <a class="w3-bar-item w3-button" href="#"></a>
</div>


<div id="nav03">
  <div class="w3-container w3-border-bottom">
    <h1 class="w3-text-theme">Game total</h1>
    <h2>"""+player_2.name+""" - """+str(player_2.score)+"""</h2>
    <h2>"""+player_1.name+""" - """+str(player_1.score)+"""</h2>
  </div>
</div>
</div>

<div class="w3-overlay w3-hide-large" onclick="w3_close()" style="cursor:pointer" id="myOverlay"></div>

<div class="w3-main" style="margin-left:300px;"> 

<div class="w3-top w3-blue w3-large w3-hide-large">
  <i class="fa fa-bars w3-button w3-blue w3-xlarge" onclick="w3_open()"></i>
</div>

<header class="w3-container w3-blue w3-padding-64 w3-center">
  <h1 class="w3-xxxlarge w3-padding-16">Dice Game</h1>
</header>

<div class="w3-container w3-padding-large w3-section w3-light-grey">
  <h1 class="w3-jumbo">Game</h1>
  <p class="w3-xlarge">Click to roll</p>
  <form class="w3-container" action="/roll/">
  <button class="w3-button w3-block w3-blue w3-section w3-padding" type="submit">Roll</button>
  </form>

</div>


<footer class="w3-container w3-padding-large w3-light-grey w3-justify w3-opacity">
  <h3>Made by Team Toad</h3>
</footer>

</div>

<script>
function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
}

function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}

openNav("nav01");
function openNav(id) {
  document.getElementById("nav01").style.display = "none";
  document.getElementById("nav02").style.display = "none";
  document.getElementById("nav03").style.display = "none";
  document.getElementById(id).style.display = "block";
}
</script>

<script src="https://www.w3schools.com/lib/w3codecolor.js"></script>

<script>
w3CodeColor();
</script>

</body>
</html>
"""

app.run("localhost", port=80)
