from time import sleep
import rpg_modules as rm
import rpg_colours as rc
import screens


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
            print(f"{rc.LIGHT_GREEN}AOE{rc.DARK_GRAY} move selected!{rc.END}")
        
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
                case c if c in attack:
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
                    screens.game_help()
                    
                case c if c == "movelist" or c == "moves":
                    game_movelist()
                    
                case _:
                    print(f"{rc.DARK_GRAY}Invalid command! Type \"{rc.RED}help{rc.DARK_GRAY}\" for commands.{rc.END}")
          
    def attack(self):
        """Opens up targeting menu"""
        
        manual_select = ManualTargetSelect(self.attackers, self.targets)
        for _, v in manual_select.selected_targets.items():
            print(f"\n{manual_select.selected_attacker.name} used {rc.LIGHT_CYAN}{manual_select.selected_move.__name__}{rc.END} on {v.name}!")
            manual_select.selected_move(v)
        
        self.selecting = False

class MainMenu:
    """Main menu class\n
    :param Int ptz: default player team size
    :param Int atz: ai team size
    :param Bool atzs: whether the ai team size was manually set
    :param Str difficulty: current difficulty
    :param List difficulties: list of available difficulties
    """
    def __init__(self, ptz: int, atz: int, atzs: False, difficulty = "easy", difficulties = list):
        self.default_player_team_size = ptz
        self.ai_team_size = atz
        self.ai_team_size_set = atzs
        self.difficulty = difficulty
        self.difficulties = difficulties

    def start_screen(self):
        """Main menu screen"""
        
        self.start_game = False
        while not self.start_game:

    
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
                case c if c in start:
                    self.start_game = True

                case c if c in settings:
                    self.settings()
            
                case "exit":
                    print(f"{rc.DARK_GRAY}You cannot escape the forest...{rc.END} ")
                    sleep(1)
                    return action

                case _:
                    print(f"{rc.LIGHT_RED}{action} is not a valid option.{rc.END}")
                    sleep(0.8)

        
    def settings(self):
        """Game settings screen

        Returns:
            int: default player team size
            int: ai team size
            bool: whether the ai team size was set
            str: difficulty
        """
    
        settings_done = False
        while not settings_done:
            print(f"\n\
Current settings:\n\n\
{rc.LIGHT_CYAN}{rc.UNDERLINE}Team Size{rc.END}\n\n\
{rc.DARK_GRAY}>{rc.END} {rc.LIGHT_CYAN}Player{rc.END}: {rc.LIGHT_GREEN}{self.default_player_team_size}{rc.END}\n\
{rc.DARK_GRAY}>{rc.END} {rc.LIGHT_CYAN}AI{rc.END}: {rc.LIGHT_GREEN}{self.ai_team_size}{rc.END}\n\n\
{rc.DARK_GRAY}>{rc.END} {rc.UNDERLINE}D{rc.END}ifficulty: {rc.LIGHT_GREEN}{self.difficulty.capitalize()}{rc.END}\n\n\
{rc.DARK_GRAY}Press {rc.RED}enter{rc.DARK_GRAY} or type {rc.RED}\"exit\"{rc.DARK_GRAY} to exit.{rc.END}")

            rm.cursor()
            setting = input(f"Choose option: ").casefold().strip()
            rm.cursor(False)

            setting_exit = ["back", "exit", "done", ""]
            player_team_size_input = ["player", "player team", "player team size"]
            ai_team_size_input = ["ai", "ai team", "ai team size"]
            difficulty_input = ["d", "diff", "difficulty"]
            match setting:
                case c if c in setting_exit:
                    settings_done = True
                
                case "start":
                    settings_done = True
                    self.start_game = True
            
                case c if c in player_team_size_input:
                    self.default_player_team_size = rm.int_checker(query = f"{rc.LIGHT_CYAN}Player team size:{rc.END} {rc.LIGHT_GREEN}")
                    print(f"{rc.END}", end = "")
                
                case c if c in ai_team_size_input:
                    self.ai_team_size = rm.int_checker(query = f"{rc.LIGHT_CYAN}AI team size:{rc.END} {rc.LIGHT_GREEN}")
                    print(f"{rc.END}", end = "")
                    self.ai_team_size_set = True
            
                case c if c in difficulty_input:
                    chosen_difficulty = input(f"Choose difficulty: {rc.LIGHT_GREEN}").casefold().strip()
                    print(f"{rc.END}", end = "")
                    
                    if chosen_difficulty not in self.difficulties:
                        print(f"{rc.LIGHT_RED}{chosen_difficulty} is not a valid difficulty.{rc.END}")
                        sleep(0.8)
                        
                    else:
                        self.difficulty = chosen_difficulty
                    
                case _:
                    print(f"{rc.LIGHT_RED}{setting} is not a valid setting.{rc.END}")
                    sleep(0.8)     
                
        return self.default_player_team_size, self.ai_team_size, self.ai_team_size_set, self.difficulty

def game_movelist():
    """Choose which movelist to print"""
    
    char_class = input(f"\n{rc.DARK_GRAY}Which class's movelist would you like to check?{rc.END} ").casefold().strip()
    
    match char_class:
        
        case c if c == "w" or c == "warrior":
            print(f"\n\
{rc.LIGHT_BLUE}Warrior{rc.END}:\n\n\
{rc.LIGHT_RED}Flurry: {rc.DARK_GRAY}Single target attack that hits 3-5 times for 30% damage each, then cloaks{rc.END}\n\
{rc.LIGHT_RED}Neutralise: {rc.DARK_GRAY}Armour-piercing attack that ignores 50% defence but does 90% damage{rc.END}\n\
{rc.LIGHT_RED}Rage: {rc.DARK_GRAY}Sacrifice 10% health to deal double damage{rc.END}\n\
{rc.LIGHT_RED}Execute: {rc.DARK_GRAY}Deals more damage the lower the enemy health is (cannot crit)\n\
{rc.LIGHT_RED}Sweep: {rc.DARK_GRAY}Leg sweep all enemies and deal damage based on their defence (cannot crit)")
        
        case c if c == "t" or c == "tank":
            print(f"\n\
{rc.LIGHT_BLUE}Tank{rc.END}:\n\n\
{rc.LIGHT_RED}Equaliser: {rc.DARK_GRAY}Deals damage based on the difference between the character's attack and the enemy's defence{rc.END}\n\
{rc.LIGHT_RED}RecklessCharge: {rc.DARK_GRAY}A risky but powerful attack that has a 20% chance to miss{rc.END}\n\
{rc.LIGHT_GREEN}Barricade: {rc.DARK_GRAY}Gives all allies the shielded state, reducing their next damage received{rc.END}")
            
        case c if c == "c" or c == "cleric":
            print(f"\n\
{rc.LIGHT_BLUE}Cleric{rc.END}:\n\n\
{rc.LIGHT_RED}Lightning: {rc.DARK_GRAY}Moderate lightning spell that hits all targets with 85% damage (cannot crit){rc.END}\n\
{rc.LIGHT_GREEN}Restoration: {rc.DARK_GRAY}Heals and revives an ally with with magic{rc.END}\n\
{rc.LIGHT_RED}Curse: {rc.DARK_GRAY}Uses the enemy's own attack to deal damage (cannot crit){rc.END}\n\
{rc.LIGHT_PURPLE}PoisonCloud: {rc.DARK_GRAY}Poisons all enemies for 2 rounds")
        
        case _:
            print(f"{rc.LIGHT_RED}{char_class}{rc.DARK_GRAY} is not a valid class!{rc.END}")

class ExitMenu:
    """Exit menu screen that checks for player confirmation before quitting"""
    def __init__(self):
        self.continue_confirmed = False
    
    def exit_select(self):
        if not self.continue_confirmed:
            exit_input = input(f"{rc.LIGHT_GREEN}Continue?{rc.DARK_GRAY} Press any key to exit or {rc.LIGHT_GREEN}\"y\"{rc.DARK_GRAY} to continue.\n{rc.END}").casefold().strip()
            yes = ["y", "yes"]
            
            match exit_input:
                case y if y in yes:
                    self.continue_confirmed = True
                
                case _:
                    self.confirm_select()
        
        if self.continue_confirmed:
            return True
        else:
            return False

    def confirm_select(self):
        confirm_input = input(f"{rc.LIGHT_RED}ARE YOU SURE? {rc.DARK_GRAY}Type \"n\" to go back.{rc.END}\n").casefold().strip()
        no = ["n", "no"]
        
        match confirm_input:
            case n if n in no:
                self.exit_select()
                
            case _:
                print(f"{rc.LIGHT_WHITE}Thanks for playing!{rc.END}")