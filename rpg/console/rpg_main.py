import sys
import random
from time import sleep
from time import perf_counter
import arcade
import rpg_sound
import menus
import rpg_modules as rm
import rpg_colours as rc

# Initialising teams
ais = {}
alive_ais = {}
players = {}
alive_players = {}

# Preparing stage defaults
stage = 1
highest_stage = 1

# Preparing game difficulty
difficulties = ["easy", "normal", "hard"]
difficulty = "easy"

# Preparing team sizes
default_player_team_size = 3 #default 3
ai_team_size = 3 #default 3
ai_team_size_set = False

# Misc.
new_game = True
play_bgm = True

# Begin logging
sys.stdout = rm.logging_function()

# Hide cursor
rm.cursor(False)


def player_victory_check(stage, highest_stage):
    """Called during both turns to determine if the player has won;
    does not check if AI has won because we do not expect to die on our turn
    (This may be changed in future)"""
    
    alive_ais = 0
    for k, char in ais.items():       
        if char.alive:
            alive_ais += 1
            
    if alive_ais == 0:
        rm.stat_printer(players, ais)
        arcade.play_sound(rpg_sound.win, 0.5 * rpg_sound.volume)
        
        # Saves highest stage
        stage += 1
        if highest_stage < stage:
            highest_stage = stage
               
        # writes traits list into save file
        save_file = f"saves/{player_name}.txt"
        with open(save_file, "w") as f:
            for k, char in players.items():

                traits = [stage,
                        highest_stage,
                        char.char_class,
                        char.name,
                        char.max_health,
                        char.attack,
                        char.defence,
                        char.exp,
                        char.rank,
                        char.prestige,
                        char.total_rank
                        ]
                
                for trait in traits:
                    f.write(f"{trait}//")
                
                # Appends a debug checksum at the end to indicate the number of items

                f.write(f"{len(traits) + 1}")
                f.write("\n")

        return f"{rc.LIGHT_GREEN}Player wins!{rc.END}"
    return False

# GAME START

if play_bgm:
    arcade.play_sound(rpg_sound.bgm, 0.2)

game_running = True
while game_running:
    
    # Starting timer
    time_start = perf_counter()
    
    # Initialising variables for each game iteration
    game_exit = False
    winner = False
    game_round = 1
        
        
    # Put this into menus.py PLEASE
    start_game = False
    while not start_game:
        
        menu_action = menus.main_menu()
        if menu_action == "settings" or menu_action == "setting":
            
            (default_player_team_size, 
            ai_team_size, 
            ai_team_size_set, 
            difficulty) = menus.settings(default_player_team_size, ai_team_size, difficulties, difficulty)
        
        elif menu_action == "start":
            start_game = True
            rm.slow_print(f"{rc.DARK_GRAY}Entering the forest... {rc.END}\n", sound = 0)
            break

    # INTRO
    
    # Checks if player name is already set from previous round
    if "player_name" not in locals():
        rm.cursor()
        player_name = input(f"{rc.LIGHT_CYAN}Player name:{rc.END} ")
        rm.cursor(False)

        if player_name == "":
            player_name = "default"

    # Attempts to load save file
    try:
        players, highest_stage, loaded_stage = rm.load_game(player_name)
        new_game = False
        
    except:
        pass
        
    # Selects stage
    if not new_game:
        stage = rm.stage_load(loaded_stage, highest_stage)
    
    # Intro sound effect and art
    arcade.play_sound(rpg_sound.intro, 1 * rpg_sound.volume)
    rm.line_print(length = 60)
    
    # Prints a house in the forest
    rm.slow_print(f"\n\
     {rc.GREEN}^  ^  ^   ^  {rc.END}  {rc.LIGHT_RED}    ___I_     {rc.GREEN} ^  ^   ^  ^  ^   ^  ^\n\
    /|\/|\/|\ /|\  {rc.END}  {rc.LIGHT_RED}  /\-_--\    {rc.GREEN}/|\/|\ /|\/|\/|\ /|\/|\\\n\
    /|\/|\/|\ /|\  {rc.END} {rc.LIGHT_RED}  /  \_-__\   {rc.GREEN}/|\/|\ /|\/|\/|\ /|\/|\\\n\
    /|\/|\/|\ /|\  {rc.END} {rc.LIGHT_RED}  |{rc.RED}[]{rc.LIGHT_RED}| {rc.RED}[] {rc.LIGHT_RED}|  {rc.GREEN} /|\/|\ /|\/|\/|\ /|\/|\\\n\n\
                  {rc.YELLOW}{rc.BOLD}    RPG GAME{rc.END}\n\
             {rc.LIGHT_WHITE}{rc.FAINT} (Role-Playing game game){rc.END}", speed = 0.003, delay = 1, sound = False)
    rm.line_print(length = 60)

    arcade.play_sound(rpg_sound.start, 0.2 * rpg_sound.volume)

    # Check if this is a new game
    if new_game:
        players: dict = rm.char_create(default_player_team_size, "Players")
        
    else:
        print(f"{rc.LIGHT_BLUE}Save successfully loaded!{rc.END}")
        sleep(0.8)
        
    # AI CHARACTER CREATION
    
    if not ai_team_size_set:
        if stage != 1:
            ai_team_size = random.choice([1, 2, 2, 2, 3, 3])
        
    ais = rm.char_create(ai_team_size, "AIs")
    
    d_add, d_mult = rm.difficulty_config(difficulty)
    rm.ai_modify(stage, ais, d_add, d_mult)
    
    # Introduction screen
    rm.slow_print(f"Welcome, {rc.LIGHT_CYAN}{player_name}{rc.END}!\n")
    rm.slow_print(f"Current Stage: {rc.LIGHT_BLUE}{stage}{rc.END}")
    rm.slow_print(f"Difficulty: {rc.LIGHT_GREEN}{difficulty.capitalize()}{rc.END}")
    sleep(0.8)

    rm.stat_printer(players, ais, slow = True, intro = True)

    # Checks if both teams have members
    if len(players) == 0:
        winner = f"{rc.RED}Woah there! No characters on player team!{rc.END}"
        print(winner)
        
    elif len(ais) == 0:
        winner = f"{rc.RED}Woah there! No characters on AI team!{rc.END}"
        print(winner)
    
    # Create game menu
    menu = menus.ActionSelect(players, ais)
    
    # Main Game Loop
    while not winner and not game_exit:
        sleep(0.8)
        print(f"\n=== ROUND {rc.YELLOW}{game_round}{rc.END} ===")
        
# ----- Player Turn -----

#                                 ,-.
#                                ("O_)
#                               / `-/
#                              /-. /
#                             /   )
#                            /   /  
#               _           /-. /
#              (_)"-._     /   )
#                "-._ "-'""( )/    
#                    "-/"-._" `. 
#                     /     "-.'._
#                    /\       /-._"-._
#     _,---...__    /  ) _,-"/    "-(_)
# ___<__(|) _   ""-/  / /   /
#  '  `----' ""-.   \/ /   /
#                )  ] /   /
#        ____..-'   //   /                       )
#    ,-""      __.,'/   /   ___                 /,
#   /    ,--""/  / /   /,-""   """-.          ,'/
#  [    (    /  / /   /  ,.---,_   `._   _,-','
#   \    `-./  / /   /  /       `-._  """ ,-'
#    `-._  /  / /   /_,'            ""--"
#        "/  / /   /"         
#        /  / /   /
#       /  / /   /  o!O
#      /  |,'   /  
#     :   /    /
#     [  /   ,'  
#     | /  ,'
#     |/,-'
#     P'
        rm.slow_print(f"[{rc.LIGHT_GREEN}PLAYER{rc.END} TURN]\n")
        
        # Show enemy intent
        ai_attacker, ai_target = rm.auto_target(ais, players)
        print(f"{rc.LIGHT_RED}{ai_attacker.name}{rc.DARK_GRAY} is planning to attack {rc.LIGHT_GREEN}{ai_target.name}{rc.END}... ")

        # Temporarily store alive units
        alive_ais: dict = rm.create_alive_dict(ais)
        
        # Player turn
        rm.status_check(players)
        menu.select()
        
        # Check how many alive enemies are now dead
        print()
        rm.check_dead(alive_ais)
                
        # Clear and prepare for next round
        alive_ais.clear()

        # Checks if AI is defeated
        # Yeah I know we can just check the same alive dict but I'm not rewriting that ¯\_(ツ)_/¯
        winner = player_victory_check(stage, highest_stage)
        if winner:
            print()
            rm.slow_print(winner)
            break

        sleep(0.8)
        rm.stat_printer(players, ais)
        
# ----- AI TURN -----
        
#                       :::!~!!!!!:.
#                   .xUHWH!! !!?M88WHX:.
#                 .X*#M@$!!  !X!M$$$$$$WWx:.
#                :!!!!!!?H! :!$!$$$$$$$$$$8X:
#               !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
#              :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
#              ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
#                !:~~~ .:!M"T#$$$$WX??#MRRMMM!
#                ~?WuxiW*`   `"#$$$$8!!!!??!!!
#              :X- M$$$$       `"T#$T~!8$WUXU~
#             :%`  ~#$$$m:        ~!~ ?$$$$$$
#           :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
# .....   -~~:<` !    ~?T#$$@@W@*?$$      /`
# W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
# #"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
# :::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
# .~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
# Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
# $R@i.~~ !     :   ~$$$$$B$$en:``
# ?MXT@Wx.~    :     ~"##*$$$$M~

        rm.slow_print(f"[{rc.LIGHT_RED}AI{rc.END} TURN]")
        
        # If the AI that was planning to attack us has died, reroll attacker and target
        rm.status_check(ais)
        if not ai_attacker.alive:
            print(f"{rc.LIGHT_RED}{ai_attacker.name}{rc.DARK_GRAY} was defeated! {rc.RED}Selecting new targets...{rc.END}")
            ai_attacker, ai_target = rm.auto_target(ais, players)
        
        rm.slow_print("." * random.randint(3, 4), *rm.slower_print)
        
        # Temporarily store alive units
        alive_players: dict = rm.create_alive_dict(players)
        
        # AI attacks
        ai_attacker.BasicAttack(ai_target)
        
        # Check how many have died after the attack
        print()
        rm.check_dead(alive_players)
        
        # Clear alive players
        alive_players.clear()
        
        # Create it again to check if there's anyone still alive
        alive_players: dict = rm.create_alive_dict(players)
        
        # Checks if there is nobody alive in player team
        if not alive_players:
            rm.stat_printer(players, ais)
            arcade.play_sound(rpg_sound.lose, 0.7 * rpg_sound.volume)
            winner = f"{rc.RED}AI wins!{rc.END}"
            print()
            rm.slow_print(winner)
            break
        
        # Clear and prepare for next round
        else:
            alive_players.clear()
        
        # Checks if AI is defeated again in case it dies on its turn
        winner = player_victory_check(stage, highest_stage)
        if winner:
            print()
            rm.slow_print(winner)
            break
        
    # Preparing for next round
        rm.stat_printer(players, ais)
        game_round += 1
        
    # Resetting game
    ais.clear()
    players.clear()
    time_stop = perf_counter()
    
    if winner == f"{rc.RED}AI wins!{rc.END}":
        print(f"Stage {stage} lost in {rc.YELLOW}{game_round}{rc.END} rounds... ({time_stop - time_start:.1f}s)")
        
    else:
        print(f"Stage {stage} won in {rc.YELLOW}{game_round}{rc.END} rounds! ({time_stop - time_start:.1f}s)")
    
    # Check if player wants to exit the game
    rm.cursor()
    game_exit = input('Game saved. Press any key to exit or \"y\" to continue.\n').casefold().strip()
    confirm = input(f"{rc.LIGHT_RED}ARE YOU SURE?{rc.END}\n")
    
    if game_exit != "yes" and game_exit != "y" and confirm != "no" and confirm != "n":
        print(f"\n{rc.LIGHT_WHITE}Thanks for playing!{rc.END}")
        game_running = False

sys.stdout.log.close()