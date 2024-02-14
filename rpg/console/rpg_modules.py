import sys
import logging
import random
from datetime import datetime
from time import sleep
import arcade
import units
import rpg_sound
import rpg_colours as rc
import menus

#speed (s), delay (s), sound_effect (int)
slower_print = (0.7, 0.2, 2, 1 * rpg_sound.volume)

# PRINT THINGS

class logging_function:
    """Logs the game output into both console and an output file"""
        
    def __init__(self):
        self.stream = sys.stdout
        self.log = open("gamelog.txt", "w", encoding = "UTF8")
        
    def write(self, data):
        current_time = datetime.now().strftime("%D %H:%M:%S")
        if data.isspace() or len(data) == 1:
            self.log.write(data)
            
        else:
            self.log.write(f"[{current_time}] {data}")
            
        self.stream.write(data)
        self.stream.flush()
        
    # Prevents flush from throwing an exception
    def flush(self):
        pass

def line_print(char = ">", length = 100):
    """Prints a line across the screen to separate text"""
    print(f"{rc.DARK_GRAY}{char * length}{rc.END} ")

# Unfortunately I can't seem to get separate and top_bar to work with functions that create objects
def separate(func):
    """Prints separator lines at the start and end of a function"""
    
    def wrapper(*args, **kwargs):
        line_print()
        func(*args, **kwargs)
        line_print("<")
        
    return wrapper

def top_bar(func):
    """Prints a smaller separator line at the start of a function"""
    
    def wrapper(*args, **kwargs):
        print()
        line_print("=", 50)
        func(*args, **kwargs)
        
    return wrapper
    
# Shows or hides the cursor    
def cursor(show = True):
    if show:
        print(f"{rc.SHOW}", end = "")
    else:
        print(f"{rc.HIDE}", end = "")

# Prints characters one at a time #speed default 0.03
def slow_print(s, speed = 0.01, delay = 0.2, sound = 1, volume = 1):
    
    # Rate of sound playback = 1/sound_delay
    sound_delay = 4
    sound_delay_counter = sound_delay
    
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        if sound == 1:
            
            # Slows the speed of sound playback
            sound_delay_counter += 1
            
            if sound_delay_counter >= 3:
                arcade.play_sound(rpg_sound.text, 1.2 * rpg_sound.volume)
                # Resets the counter
                sound_delay_counter = 0
        
        elif sound == 2:
            arcade.play_sound(rpg_sound.text_2, 0.5 * rpg_sound.volume)
        
        sleep(speed)

    sleep(delay)
    sys.stdout.write("\n")

# Prints stats of both teams
@separate
def stat_printer(players: dict, enemies: dict, slow = False, intro = False):

    for k, v in players.items():
        if v.alive is True:
            if intro:
                arcade.play_sound(rpg_sound.ready, 0.1 * rpg_sound.volume)
                print(f"{rc.LIGHT_GREEN}Human {k}:{rc.END}")
                sleep(0.1)
            if slow:
                v.stats(True)
                
            else:
                v.stats()
    
    # Fake AI loading characters effect        
    if intro:
        line_print()
        print(f"{rc.DARK_GRAY}", end = "")
        slow_print("." * random.randint(3, 4), *slower_print)
        print(f"{rc.END}", end = "")
        line_print("<")
        
    else:      
        print(f"{rc.DARK_GRAY}{'----------------------------------------------':^100}{rc.END}")

    for k, v in enemies.items():
        if v.alive is True:
            if intro:
                arcade.play_sound(rpg_sound.ready, 0.1 * rpg_sound.volume)
                print(f"{rc.LIGHT_RED}AI {k}:{rc.END}")
                sleep(0.1)
                
            if slow:
                v.stats(True)
                
            else:
                v.stats()

# CHECK THINGS

def int_checker(input_query = None, query = False):
    """Forces the user to enter an integer"""
    
    valid = False
    while not valid:
        if query:
            input_query = input(query).casefold().strip()
            
            if input_query == "exit" or input_query == "back":
                return False
        
        try:
            result = int(input_query)
            valid = True
            return result
        
        except:
            print(f"{rc.RED}ERROR: {rc.DARK_GRAY}Please enter an integer.{rc.END} ")

def check_dead(alive_members: dict):
    for _, v in alive_members.items():
        if not v.alive:
            arcade.play_sound(rpg_sound.death, 1 * rpg_sound.volume)
            slow_print(f"{v.name} {rc.DARK_GRAY}has been {rc.LIGHT_RED}defeated... {rc.END}")
            sleep(0.8)

# CREATE THINGS

def create_alive_dict(team: dict):
    """Creates a dictionary of alive units"""
    
    # Creates a new dictionary of alive members
    alive: dict = {}
    
    # Adds the key and object of the unit to alive dict
    try:
        for key, unit in team.items():
            if unit.alive:
                alive[key] = unit
    
    except TypeError ("Feed player dictionaries into me!"):
        pass
    
    except IndexError(f"Team {team} is not set up properly. Please ensure it is configured correctly"):
        pass
    
    except:
        logging.error("Error with create_alive_dict!")
    
    return alive

# Create subclass units
def class_creator(class_name: str, name: str, team: str):
    """Create character objects based on their class

    Args:
        class_name (str): Name of the character's class
        name (str): Name of the character
        team (str): Character's team name

    Returns:
        object: Character object
    """
    
    if class_name == "Warrior":
        character = units.Warrior(name, team)
    
    elif class_name == "Tank":
        character = units.Tank(name, team)
        
    elif class_name == "Cleric":
        character = units.Cleric(name, team)

    return character

# Create a new character, returns a dictionary
def char_create(team_size: int, team: str):
    """Create a new character

    Args:
        team_size (int): Number of characters to create
        team (str): Name of team to create characters for

    Returns:
        dict: Dictionary of created characters
    """
    
    created_chars = {}

    # If team is players, we ask for input
    if team == "Players":
        for char in range(1, team_size + 1):
            print(f"{rc.ITALIC}Please create {rc.YELLOW}{team_size - char + 1}{rc.END} {rc.ITALIC}character(s)... {rc.END}\n")
            
            cursor()
            name = input(f"Character {char} {rc.LIGHT_GREEN}name{rc.END}:\n")
            
            char_class = units.class_filter(input(f"{rc.LIGHT_BLUE}Class {rc.END}(\
{rc.LIGHT_CYAN}W{rc.LIGHT_GRAY}arrior/\
{rc.LIGHT_CYAN}T{rc.LIGHT_GRAY}ank/\
{rc.LIGHT_CYAN}C{rc.LIGHT_GRAY}leric\
{rc.END}): \n"))
            
            # For aesthetics
            cursor(False)
            line_print(length = 50)
            
            # Creates class based on selected class
            character = class_creator(char_class, name, team)
            created_chars[char] = character
    
    # If team is AIs we randomly generate
    elif team == "AIs":
        for char in range(1, team_size + 1):
            name = f"AI{str(random.randint(1,100))}"
            char_class = random.choice(units.classes)
            
            # Creates class based on selected class
            character = class_creator(char_class, name, team)
            created_chars[char] = character
                
    return created_chars

# GAME SETUP

#         __I__
#    .-'"  .  "'-.
#  .'  / . ' . \  '.
# /_.-..-..-..-..-._\ .---------------------------------.
#          #  _,,_   ( I hear it might rain people today )
#          #/`    `\ /'---------------------------------'
#          / / 6 6\ \
#          \/\  Y /\/       /\-/\
#          #/ `'U` \       /a a  \               _
#        , (  \   | \     =\ Y  =/-~~~~~~-,_____/ )
#        |\|\_/#  \_/       '^--'          ______/
#        \/'.  \  /'\         \           /
#         \    /=\  /         ||  |---'\  \
#    jgs  /____)/____)       (_(__|   ((__|

def load_game(player_name: str):
    """_summary_

    Args:
        player_name (str): Name of the player

    Returns:
        tuple: created_chars (dict), highest_stage (int), loaded_stage (int)
    """
    try:
        with open(f"saves/{player_name}.txt", "r") as f:
            
            created_chars = {}
            
            # Helps us number our characters
            char_count = 0
            
            # For each character in the file
            for line in f:
                char_count += 1
                loaded_values = line.split("//")

                # Initialising characters
                character = class_creator(loaded_values[2], loaded_values[3], "Players")

                # Loading the rest of our character attributes
                character.max_health = float(loaded_values[4])
                character.health = int(character.max_health)  # fully heals character
                character.attack = float(loaded_values[5])
                character.defence = float(loaded_values[6])
                character.exp = int(loaded_values[7])
                character.rank = int(loaded_values[8])
                character.prestige = int(loaded_values[9])
                character.total_rank = int(loaded_values[10])

                # Resets character states
                character.hidden = False
                character.alive = True
                
                # Sets character max exp back
                character.max_exp = int(units.BASE_MAX_EXP * units.EXP_SCALING ** (character.total_rank - 1))
                
                # Adds character into created characters list
                created_chars[char_count] = character
                
                # Loads the highest stage
                highest_stage = int(loaded_values[1])
                
                # Load the last saved stage
                loaded_stage = int(loaded_values[0])
            
            slow_print(f"{rc.LIGHT_GREEN}{char_count} character(s){rc.DARK_GRAY} detected for {rc.LIGHT_CYAN}{player_name}{rc.DARK_GRAY}. Loading... {rc.END}")
                    
        return created_chars, highest_stage, loaded_stage
    
    except FileNotFoundError:
        slow_print(f"{rc.DARK_GRAY}No save file detected for {rc.BROWN}{player_name}{rc.DARK_GRAY}{rc.END}\nStarting new game!", sound = 0)
        sleep(0.5)
        menus.game_help()
        sleep(1.5)
        
    except:
        print(f"{rc.RED}Error while loading {player_name}. RZ probably broke the save system again{rc.END}")
        sleep(0.8)
    
# Select stage
def stage_load(loaded_stage: int, highest_stage: int):
    """_summary_

    Args:
        loaded_stage (int): Previous stage recorded in game file
        highest_stage (int): Highest stage recorded in game file

    Returns:
        int: Stage to set game to
    """

    slow_print(f"Highest stage: {highest_stage}")

    stage_load_check = input(f"Continue from Stage {loaded_stage}? ").casefold().strip()
    
    try:
        stage_load_check = int(stage_load_check)
        
    except:
        pass
    
    if isinstance(stage_load_check, int):
        stage = stage_load_check
        
    elif stage_load_check == "yes" or stage_load_check == "y" or stage_load_check == "":
        stage = loaded_stage

    else:
        stage = int_checker(query = f"Which {rc.YELLOW}stage{rc.END} would you like to load? ")
        if stage <= 0:
            slow_print(f"{rc.DARK_GRAY}You cannot set {rc.RED}negative stage numbers.{rc.END} Defaulting to {rc.YELLOW}stage 1{rc.END}!")
            stage = 1

    slow_print(f"{rc.DARK_GRAY}Initialising {rc.LIGHT_BLUE}Stage {stage}... {rc.END}")
    sleep(0.8)
    
    return stage

def difficulty_config(difficulty: str):
    if difficulty == "easy":
        d_add = 0
        d_mult = 1
    
    elif difficulty == "normal":
        d_add = 1
        d_mult = 1.2
        
    elif difficulty == "hard":
        d_add = 2
        d_mult = 1.4
        
    return d_add, d_mult

# GAMEPLAY

def auto_setup():
    """Choose how many rounds we want to automatically play

    Returns:
        int: number of auto rounds
    """
    
    rounds = int_checker(query = f"Number of auto rounds ({rc.LIGHT_BLUE}0{rc.END} for infinite): \n")
        
    if rounds <= 0:
        rounds = 99999
        with open("automsg.txt", "r") as f:
            auto_msg = random.choice(f.readlines()).strip()
            print(f"{rc.DARK_GRAY}", end = "")
            slow_print(auto_msg)
            print(f"{rc.END}", end = "")
    else:
        slow_print(f"{rc.DARK_GRAY}Activating neural enhancements for {rc.LIGHT_BLUE}{rounds}{rc.DARK_GRAY} rounds... {rc.END}")
    print(f"{rc.CYAN}")
    slow_print("." * 3, 1, 0.25, 2)
    print(f"{rc.END}")
    arcade.play_sound(rpg_sound.auto, 0.5 * rpg_sound.volume)
    sleep(1.5)
    slow_print(f"Success!\n")
    
    return rounds

def ai_modify(stage: int, team: dict, d_add = 0, d_mult = 1):
    """Modify AI stats according to difficulty and stage

    Args:
        stage (int): Current stage
        team (dict): Dictionary of objects
        d_add (int, optional): Bonus ranks to add. Defaults to 0.
        d_mult (int, optional): Multiply bonus ranks. Defaults to 1.
    """
    
    for _, v in team.items():
        v.rank_up(int((stage - 1 + d_add) * d_mult), False)
        v.max_exp = int(units.BASE_MAX_EXP * units.EXP_SCALING ** (v.total_rank - 1))
        
        # Fully heal character after ranking up
        v.health = v.max_health

def auto_target(attackers: dict, targets: dict):
    """AI targeting algorithm"""
    
    # Creates dictionaries for our alive units
    alive_attackers: dict = create_alive_dict(attackers)
    alive_targets: dict = create_alive_dict(targets)
    
    # In case our game is still running after everyone is dead
    if len(alive_attackers) > 0 and len(alive_targets) > 0:
        
        attacker: object = random.choice(list(alive_attackers.values()))
        target: object = random.choice(list(alive_targets.values()))
        
        # Returns the attacker and target unit object
        return attacker, target
    
    else:
        raise ValueError(f"If you reach this error, it means the world is about to endc")
    
def status_check(team: dict):
    """Updates status of characters in a team

    Args:
        team (dict): Dictionary of objects
    """
    for _, v in team.items():
        if v.poisoned > 0:
            arcade.play_sound(rpg_sound.poison)
            print(f"\
{v.name}{rc.DARK_GRAY} has lost {rc.LIGHT_RED}{int(v.health * 0.1)}{rc.DARK_GRAY} \
health from {rc.LIGHT_PURPLE}poison{rc.DARK_GRAY}...{rc.END}")
            v.health *= 0.9
            v.death_check()
            v.poisoned -= 1
            sleep(0.4)
            
            if v.poisoned == 0:
                print(f"{v.name}{rc.DARK_GRAY} has {rc.LIGHT_GREEN}recovered{rc.END}!\n")
            
            else:
                print(f"\
{v.name}{rc.DARK_GRAY} is still {rc.LIGHT_PURPLE}poisoned{rc.DARK_GRAY} \
for {rc.LIGHT_PURPLE}{v.poisoned}{rc.DARK_GRAY} \
more turn(s)!{rc.END}\n")
        
        sleep(0.8)