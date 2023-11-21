from time import sleep
import units
import rpg_modules as rpgm
import rpg_colours as rc
import screens

def load_game(player_name: str):
    """Attempts to load characters from a player's save file

    Args:
        player_name (str): Name of the player

    Returns:
        tuple: created_chars (dict), highest_stage (int), loaded_stage (int)
    """
    try:
        with open(f"saves/{player_name}.txt", "r") as f:
            
            created_chars = {}
            
            # Helps us number our characters because what's enumerate anyway
            char_count = 0
            
            # For each character in the file
            for line in f:
                char_count += 1
                loaded_values: list = line.split("//")
                values = []
                
                for i in loaded_values:
                    value = i.split(": ")
                    values.append(value[1])

                # Initialising characters
                character = rpgm.class_creator(values[2], values[3], "Players")

                # Loading the rest of our character attributes
                character.max_health = int(values[4])
                character.health = int(character.max_health)  # fully heals character
                character.base_attack = int(values[5])
                character.attack = float(values[6])
                character.base_defence = int(values[7])
                character.defence = float(values[8])
                character.exp = int(values[9])
                character.rank: int = int(values[10])
                character.prestige = int(values[11])
                character.total_rank = int(values[12])

                # Resets character states
                character.hidden = False
                character.alive = True
                
                # Sets character max exp back
                character.max_exp = int(units.BASE_MAX_EXP * units.EXP_SCALING ** (character.total_rank - 1))
                
                # Adds character into created characters list
                created_chars[char_count] = character
                
                # Loads the highest stage
                highest_stage = int(values[1])
                
                # Load the last saved stage
                loaded_stage = int(values[0])
            
            rpgm.slow_print(f"{rc.LIGHT_GREEN}{char_count} character(s){rc.DARK_GRAY} detected for {rc.LIGHT_CYAN}{player_name}{rc.DARK_GRAY}. Loading... {rc.END}")
                    
        return created_chars, highest_stage, loaded_stage
    
    except FileNotFoundError:
        rpgm.slow_print(f"{rc.DARK_GRAY}No save file detected for {rc.BROWN}{player_name}{rc.DARK_GRAY}{rc.END}\nStarting new game!", sound = 0)
        sleep(0.5)
        
        # Prints help screen for new players
        screens.game_help()
        sleep(1.5)
        
    except:
        print(f"{rc.RED}Error while loading {player_name}. Xier probably broke the save/load system again{rc.END}")
        sleep(0.8)

def save_game(player_name: str, players: dict, stage: int, highest_stage: int):
    """Saves player characters' stats into the player's save file"""

    save_file = f"saves/{player_name}.txt"
    with open(save_file, "w") as f:
        for k, char in players.items():

            stats = [f"stage: {stage}",
                    f"highest: {highest_stage}",
                    f"class: {char.char_class}",
                    f"name: {char.name}",
                    f"health: {int(char.max_health)}",
                    f"base attack: {char.base_attack}",
                    f"attack: {char.attack}",
                    f"base defence: {char.base_defence}",
                    f"defence: {char.defence}",
                    f"exp: {char.exp}",
                    f"rank: {char.rank}",
                    f"prestige: {char.prestige}",
                    f"level: {char.total_rank}" 
                    ]
            
            for stat in stats:
                f.write(f"{stat}//")
            
            # Appends a debug checksum at the end to indicate the number of items

            f.write(f"check: {len(stats) + 1}")
            f.write("\n")

def stage_load(loaded_stage: int, highest_stage: int):
    """_summary_

    Args:
        loaded_stage (int): Previous stage recorded in game file
        highest_stage (int): Highest stage recorded in game file

    Returns:
        int: The stage we will set our game to
    """

    rpgm.slow_print(f"Highest stage: {highest_stage}")

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
        stage = rpgm.int_checker(query = f"Which {rc.YELLOW}stage{rc.END} would you like to load? ")
        if stage <= 0:
            rpgm.slow_print(f"{rc.DARK_GRAY}You cannot set {rc.RED}negative stage numbers.{rc.END} Defaulting to {rc.YELLOW}stage 1{rc.END}!")
            stage = 1

    rpgm.slow_print(f"{rc.DARK_GRAY}Initialising {rc.LIGHT_BLUE}Stage {stage}... {rc.END}")
    sleep(0.8)
    
    return stage