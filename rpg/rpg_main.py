import sys
import random
from time import sleep
from time import perf_counter
import arcade
import rpg_sound as rs
import menus
import screens
import rpg_modules as rm
import rpg_colours as rc
import rpg_saveload as rsl

# Initialising teams
ais = {}
players = {}

# Preparing stage defaults
stage = 1
highest_stage = 1

# Preparing game difficulty
difficulties = ["easy", "normal", "hard"]
difficulty = "easy"

# Preparing team sizes
default_player_team_size = 3 # default is 3
ai_team_size = 3 # default is 3
ai_team_size_set = False

# Misc.
new_game = True
play_bgm = True

# Begin logging
sys.stdout = rm.logging_function()

# Hide cursor
rm.cursor(False)

# GAME START

if play_bgm:
    arcade.play_sound(rs.bgm, 0.2)

game_running = True
while game_running:
    
    # Starting timer
    time_start = perf_counter()
    
    # Initialising variables for each game iteration
    game_exit = False
    winner = False
    game_round = 1
    
    # Initialising main menu class
    mm = menus.MainMenu(default_player_team_size, ai_team_size, ai_team_size_set, difficulty, difficulties)    
    
    # Calling the start screen method
    mm.start_screen()
    
    # Updating our variables from the properties stored in the class
    default_player_team_size = mm.default_player_team_size
    ai_team_size = mm.ai_team_size
    ai_team_size_set = mm.ai_team_size_set
    difficulty = mm.difficulty
    
    # Intro text
    rm.slow_print(f"{rc.DARK_GRAY}Entering the forest... {rc.END}\n", sound = 0)
    
    # Checks if we're continuing from a previous round
    if "player_name" not in locals():
        rm.cursor()
        player_name = input(f"{rc.LIGHT_CYAN}Player name:{rc.END} ")
        rm.cursor(False)

        if player_name == "":
            player_name = "default"

    # Attempts to load save file
    try:
        players, highest_stage, loaded_stage = rsl.load_game(player_name)
        stage = rsl.stage_load(loaded_stage, highest_stage)
        new_game = False
        
    except:
        pass
    
    # Intro sound effect and art
    arcade.play_sound(rs.intro, 1 * rs.volume)
    
    screens.alt_forest()
    
    arcade.play_sound(rs.start, 0.2 * rs.volume)

    # Check if this is a new game
    if new_game:
        players: dict = rm.char_create(default_player_team_size, "Players")
        
    else:
        print(f"{rc.LIGHT_BLUE}Save successfully loaded!{rc.END}")
        sleep(0.6)
        
    # AI CHARACTER CREATION
    
    if not ai_team_size_set:
        if stage != 1:
            ai_team_size = random.choice([1, 2, 2, 2, 2, 3, 3, 3, 3, 4])
        
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
        
        # Temporarily store alive units
        alive_ais: dict = rm.create_alive_dict(ais)
        alive_players:dict = rm.create_alive_dict(players)
        
        # Show enemy intent
        ai_attacker, ai_target = rm.auto_target(alive_ais, alive_players)
        print(f"{rc.LIGHT_RED}{ai_attacker.name}{rc.DARK_GRAY} is planning to attack {rc.LIGHT_GREEN}{ai_target.name}{rc.END}... ")
        
        # Player turn
        rm.status_check(players)
        menu.select()
        
        # Check how many alive characters are now dead
        print()
        rm.check_dead(alive_ais)
        rm.check_dead(alive_players)
                
        # Clear and prepare for next round
        alive_ais.clear()
        alive_players.clear()

        # Checks if all AI characters are dead
        if not (rm.create_alive_dict(ais)):
            rm.stat_printer(players, ais)
            winner = rm.player_victory(player_name, players, stage, highest_stage)
            break
        
        # Then checks if all player characters are dead in case the AI has damage reflect or something
        if not rm.create_alive_dict(players):
            rm.stat_printer(players, ais)
            arcade.play_sound(rs.lose, 0.7 * rs.volume)
            winner = f"{rc.LIGHT_RED}AI wins!{rc.END}"
            rm.slow_print(f"\n{winner}")
            break
        
        else:
            sleep(0.6)
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

        rm.slow_print(f"[{rc.LIGHT_RED}AI{rc.END} TURN]\n")
        
        # Temporarily store alive units
        alive_players: dict = rm.create_alive_dict(players)
        alive_players: dict = rm.create_alive_dict(ais)
        
        # If the AI that was planning to attack us has died, reroll attacker and target
        rm.status_check(ais)
        if not ai_attacker.alive:
            print(f"{rc.LIGHT_RED}{ai_attacker.name}{rc.DARK_GRAY} was defeated! {rc.RED}Selecting new targets...{rc.END}\n")
            ai_attacker, ai_target = rm.auto_target(ais, players)
        
        # AI attacks
        ai_attacker.BasicAttack(ai_target)
        
        # Check how many have died after the attack
        print()
        rm.check_dead(alive_players)
        rm.check_dead(alive_ais)
        
        # Clear alive players
        alive_players.clear()
        alive_ais.clear()
        
        # Checks if all player characters are dead
        if not rm.create_alive_dict(players):
            rm.stat_printer(players, ais)
            arcade.play_sound(rs.lose, 0.7 * rs.volume)
            winner = f"{rc.LIGHT_RED}AI wins!{rc.END}"
            rm.slow_print(f"\n{winner}")
            break
        
        # Then checks AI characters as well because player's damage reflect etc. might have killed them
        if not (rm.create_alive_dict(ais)):
            rm.stat_printer(players, ais)
            winner = rm.player_victory(player_name, players, stage, highest_stage)
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
    
    exit_menu = menus.ExitMenu()
    game_running = exit_menu.exit_select()
            
sys.stdout.log.close()