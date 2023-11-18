import rpg_modules as rm
import rpg_colours as rc
from time import sleep

# Player move selection
class ManualTargetSelect:
    """Player target selection menu\n
    :param Dict attackers: Dictionary of objects
    :param Dict enemies: Dictionary of objects
    """

    def __init__(self, attackers: dict, enemies: dict):
        
        self.attackers: dict = attackers
        self.enemies: dict = enemies
        
        self.selected_attack: object = False
        self.selected_targets: dict = {}
        
        self.valid_attackers: dict = {}
        self.valid_targets: dict = {}
        self.selection_complete = False
        
        # I learned about state machines just as I finished writing this ^_^ kms
        while not self.selection_complete:
            
            while not self.selected_attack:
                self.select_attacker()
            
            while not self.selected_targets:
                self.select_target(self.selected_move)
                
            if self.selected_attacker and self.selected_targets:
                self.selection_complete = True           
                 
    def select_attacker(self):
        """Choose an alive character to perform an action"""
        
        self.valid_attackers.clear()
        
        # Displays available characters
        for k, v in self.attackers.items():
            if v.alive:
                print(f"{k}: {rc.LIGHT_GREEN}{v.name}{rc.END} ATK: {rc.LIGHT_RED}{int(v.attack)}{rc.END} {rc.LIGHT_BLUE}{v.char_class}{rc.END} ")
                
                # If attacker is alive, add it to valid attackers
                self.valid_attackers[k]: dict = v
        
        attacker_selection = rm.int_checker(query = "\nChoose attacker: ")
        
        # Checks if the selected attacker is valid
        if attacker_selection in self.attackers:
            
            # Sets the attacker
            self.selected_attacker: object = self.attackers[attacker_selection]
            
            print(f"\n{self.selected_attacker.name}'s movelist: ")
            
            # Sets the selected move
            self.selected_move: function = self.select_move(self.selected_attacker)
            self.selected_attack = True

        else:
            print(f"Invalid attacker selected, try again!")
        
    def select_move(self, unit):
        """Displays selected character's movelist"""
        
        move_selected = False
        while not move_selected:            
            
            # Displays available moves
            for k, move in unit.movelist.items():
                print(f"{k}: {rc.LIGHT_CYAN}{move.__name__}{rc.END}")
            
            # Repeats until player chooses a valid move
            move = rm.int_checker(query = "\nSelect move: ")
            if move in unit.movelist:
                move: function = unit.movelist.get(move)
                move_selected = True
                
            else:
                print("Invalid move selected, try again!")
        return move
    
    def select_target(self, move):
        """Choose target to use the move on"""
        
        self.valid_targets.clear()
        self.selected_targets.clear()
        
        hostile, aoe = move(False)
        
        # If the move is hostile
        if hostile:
            for k, v in self.enemies.items():
                if v.alive:
                    if not aoe:
                        print(f"\
{k}: {rc.LIGHT_RED}{v.name}{rc.END} \
HP: {rc.LIGHT_GREEN}{int(v.health)}{rc.DARK_GRAY}/{int(v.max_health)}{rc.END} \
DEF: {rc.LIGHT_CYAN}{int(v.defence)}{rc.END} \
ATK: {rc.LIGHT_RED}{int(v.attack)}{rc.END}")
                    
                    # If target is alive, add it to valid targets
                    self.valid_targets[k]: dict = v
                    
        # If the move is friendly
        else:
            for k, v in self.attackers.items():
                if v.alive:
                    if not aoe:
                        print(f"{k}: {rc.LIGHT_GREEN}{v.name}{rc.END} Health: {rc.LIGHT_GREEN}{int(v.health)}/{int(v.max_health)}{rc.END}")
                
                # If character is dead, append (DEAD)
                else:
                    if not aoe:
                        print(f"{rc.DARK_GRAY}{k}: {v.name} {rc.LIGHT_RED}(DEAD){rc.END} ")
                    
                    # Adds all targets
                self.valid_targets[k]: dict = v

        # If move is an AOE move, select all targets
        if aoe:
            self.selected_targets: dict = self.valid_targets
            print(f"AOE move selected!")
        
        else:
            target_selection = rm.int_checker(query = f"\nChoose target to use {rc.LIGHT_CYAN}{move.__name__}{rc.END} on: ")
        
        # Checks if our target is valid
            if target_selection in self.valid_targets:
                
                # Sets the target to arbitrary key since we only have one
                self.selected_targets[0]: dict = self.valid_targets[target_selection]

                for k, v in self.selected_targets.items():
                    print(f"Selected target {v.name}")    
                    
class ActionSelect:
    """Selecting an action during the start of player turn\n
    :param Dict attackers: Dictionary of objects
    :param Dict enemies: Dictionary of objects
    """
    
    def __init__(self, attackers: dict, targets: dict):
        
        self.attackers: dict = attackers
        self.targets: dict = targets
        self.selecting = True
        self.auto_rounds = 0
    
    def select(self):
        """Select an action"""
        
        self.selecting = True
        
        if self.auto_rounds > 0:
            attacker, target = rm.auto_target(self.attackers, self.targets)
            attacker.BasicAttack(target)
            self.auto_rounds -= 1
            self.selecting = False
        
        while self.selecting:
            rm.cursor()
            action = input(f"{rc.DARK_GRAY}\nEnter \"{rc.RED}help{rc.DARK_GRAY}\" to see all commands.{rc.END}\nYour move (leave blank to attack): ").casefold().strip()
            rm.cursor(False)
            attack = ["a", "attack", ""]
            
            match action:
                case i if i in attack:
                    self.attack()
                    break
                
                case "auto":
                    self.auto_rounds = rm.auto_setup()
                    
                    # This is so it also attacks after auto is selected and not only at the start of the turn
                    attacker, target = rm.auto_target(self.attackers, self.targets)
                    attacker.BasicAttack(target)
                    
                    self.auto_rounds -= 1
                    self.selecting = False
                    break
                
                case "stats":
                    rm.stat_printer(self.attackers, self.targets)
                
                case "help":
                    game_help()

                case _:
                    print(f"{rc.DARK_GRAY}Invalid command! Type \"{rc.RED}help{rc.DARK_GRAY}\" for commands.{rc.END}")
          
    def attack(self):
        """Opens up targeting menu"""
        
        manual_select = ManualTargetSelect(self.attackers, self.targets)
        for _, v in manual_select.selected_targets.items():
            print(f"\n{manual_select.selected_attacker.name} used {rc.LIGHT_CYAN}{manual_select.selected_move.__name__}{rc.END} on {v.name}!")
            manual_select.selected_move(v)
        
        self.selecting = False
        
def main_menu():
    """Main menu screen"""
    
    print(f"\n\
{rc.LIGHT_CYAN}Main Menu{rc.END}\n\n\
> {rc.LIGHT_GREEN}Start{rc.END}\n\
> {rc.LIGHT_GRAY}Settings{rc.END}\n"
    )

    rm.cursor()
    action = input(f"{rc.LIGHT_CYAN}Choose option:{rc.END} ").casefold().strip()
    rm.cursor(False)

    start = ["s", "start", "p", "play", ""]
    settings = ["settings", "setting"]
    match action:
        case i if i in start:
            selected = "start"
            return selected

        case i if i in settings:
            return "settings"
    
        case "exit":
            print(f"{rc.DARK_GRAY}You cannot escape the forest...{rc.END} ")
            sleep(1)
            return action

        case _:
            print(f"{rc.LIGHT_RED}{action} is not a valid option.{rc.END}")
            
    sleep(0.8)

def game_help():
    """Prints game help"""
    
    print(f"\n\
{rc.LIGHT_WHITE}HELP MENU{rc.END}\n\n\
{rc.LIGHT_RED}attack/a{rc.DARK_GRAY} - {rc.END}choose attack\n\
{rc.LIGHT_BLUE}auto{rc.DARK_GRAY} - {rc.END}automatically attack\n\
{rc.BROWN}stats{rc.DARK_GRAY} - {rc.END}displays stats\n\
{rc.LIGHT_GREEN}help{rc.DARK_GRAY} - {rc.END}displays this screen\
")

def settings(
    default_player_team_size: int,
    ai_team_size: int,
    difficulties: list,
    difficulty = "easy"
):
    """Game settings screen

    Args:
        default_player_team_size (int): Default number of players (only for new game)
        ai_team_size (int): AI team size
        difficulties (list): List of available difficulties
        difficulty (str, optional): Current difficulty. Defaults to "easy".
    """
    
    ai_team_size_set = False
    
    settings_done = False
    while not settings_done:
        print(f"\n\
Current settings:\n\n\
{rc.LIGHT_CYAN}{rc.UNDERLINE}Team Size{rc.END}\n\n\
{rc.DARK_GRAY}>{rc.END} {rc.LIGHT_CYAN}Player{rc.END}: {rc.LIGHT_GREEN}{default_player_team_size}{rc.END}\n\
{rc.DARK_GRAY}>{rc.END} {rc.LIGHT_CYAN}AI{rc.END}: {rc.LIGHT_GREEN}{ai_team_size}{rc.END}\n\n\
{rc.DARK_GRAY}>{rc.END} {rc.UNDERLINE}D{rc.END}ifficulty: {rc.LIGHT_GREEN}{difficulty.capitalize()}{rc.END}\n\n\
{rc.DARK_GRAY}Press {rc.RED}enter{rc.DARK_GRAY} or type {rc.RED}\"exit\"{rc.DARK_GRAY} to exit.{rc.END}")

        rm.cursor()
        setting = input(f"Choose option: ").casefold().strip()
        rm.cursor(False)

        setting_exit = ["back", "exit", "done", ""]
        player_team_size_input = ["player", "player team", "player team size"]
        ai_team_size_input = ["ai", "ai team", "ai team size"]
        difficulty_input = ["d", "diff", "difficulty"]
        match setting:
            case i if i in setting_exit:
                settings_done = True
        
            case i if i in player_team_size_input:
                default_player_team_size = rm.int_checker(query = f"{rc.LIGHT_CYAN}Player team size:{rc.END} {rc.LIGHT_GREEN}")
                print(f"{rc.END}", end = "")
            
            case i if i in ai_team_size_input:
                ai_team_size = rm.int_checker(query = f"{rc.LIGHT_CYAN}AI team size:{rc.END} {rc.LIGHT_GREEN}")
                print(f"{rc.END}", end = "")
                ai_team_size_set = True
        
            case i if i in difficulty_input:
                chosen_difficulty = input(f"Choose difficulty: {rc.LIGHT_GREEN}").casefold().strip()
                print(f"{rc.END}", end = "")
                
                if chosen_difficulty not in difficulties:
                    print(f"{rc.LIGHT_RED}{chosen_difficulty} is not a valid difficulty.{rc.END}")
                    sleep(0.8)
                    
                else:
                    difficulty = chosen_difficulty
                
            case _:
                print(f"{rc.LIGHT_RED}{setting} is not a valid setting.{rc.END}")
                sleep(0.8)     
            
    return default_player_team_size, ai_team_size, ai_team_size_set, difficulty