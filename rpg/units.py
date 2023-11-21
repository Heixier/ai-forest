import random
from time import sleep
import arcade
import rpg_modules as rm
import rpg_colours as rc
import rpg_sound as rs

#PARAMETERS
classes = ["Warrior", "Tank", "Cleric"]

MAX_HEALTH = 100 # default = 100
BASE_MAX_EXP = 100 # default = 100

# (For future reference) Formula for log growth: BASE_MAX_EXP + EXP_SCALING * math.log(self.total_rank)
EXP_SCALING = 1.028

# Character class stats and scaling
# Formula: self.attack = BASE_ATK + (ATK * ATK_SCALE ** (self.total_rank  -1))

# Warrior base stats
W_BASE_ATK = (5, 20)
W_ATK = 15

W_BASE_DEF = (1, 10)
W_DEF = 5

# Warrior scaling
W_ATK_SCALE = 1.023
W_DEF_SCALE = 1.016
W_HEALTH_SCALE = 1.02

# Tank base stats
T_BASE_ATK = (1, 10)
T_ATK = 5

T_BASE_DEF = (5, 15)
T_DEF = 10

# Tank scaling
T_ATK_SCALE = 1.025
T_DEF_SCALE = 1.019
T_HEALTH_SCALE = 1.023

# Cleric base stats
C_BASE_ATK = (10, 25)
C_ATK = 17.5

C_BASE_DEF = (1, 5)
C_DEF = 2.5

# Cleric scaling
C_ATK_SCALE = 1.023
C_DEF_SCALE = 1.018
C_HEALTH_SCALE = 1.016

# Critical chance
CRIT_CHANCE = int(1 / 0.25)
CRIT_MULTIPLIER = 1.5

# Character ranks
CHAR_RANKS = {\
    1: f"{rc.DARK_GRAY}Iron{rc.END}", 
    2: f"{rc.DARK_GRAY}Bronze{rc.END}", 
    3: f"{rc.LIGHT_GRAY}Silver{rc.END}", 
    4: f"{rc.YELLOW}Gold{rc.END}", 
    5: f"{rc.LIGHT_WHITE}Platinum{rc.END}", 
    6: f"{rc.LIGHT_GREEN}Emerald{rc.END}", 
    7: f"{rc.LIGHT_CYAN}Diamond{rc.END}", 
    8: f"{rc.LIGHT_BLUE}Master{rc.END}", 
    9: f"{rc.LIGHT_PURPLE}Grandmaster{rc.END}", 
    10: f"{rc.LIGHT_RED}Challenger{rc.END}"
}

def class_filter(input: str):
    """Input validation for character class selection"""
    
    input = input.casefold()\
        .strip()\
        .capitalize()

    match input:
        
        case "W":
            input = "Warrior"
            
        case "T":
            input = "Tank"
            
        case "C":
            input = "Cleric"
        
    if input not in classes:
        default = random.choice(classes)
        print(f"{rc.DARK_GRAY}Invalid class. {rc.LIGHT_RED}{default}{rc.DARK_GRAY} has automatically been selected!{rc.END}")
        input = default
        
    return input

class unit:
    """Parent class for character classes; does nothing."""
    
    def __init__(self, name: str, team: str):
        
        #Sets name to "Default" if left blank
        
        if len(name) <= 0:
            name = "Human" + str(random.randint(1, 100))
            
        self.name = name
        self.health = MAX_HEALTH
        self.max_health = MAX_HEALTH
        self.rank = 1
        self.total_rank = 1
        self.exp = 0
        self.max_exp = int(BASE_MAX_EXP * EXP_SCALING ** (self.total_rank - 1))
        self.prestige = 0
        
        self.alive = True
        self.team = team
        self.movelist = {1: self.BasicAttack}
        
        self.shielded = False
        self.cloaked = False
        self.poisoned = 0

# STAT MODIFIERS
        
    def rank_up(self, increment = 0, announce = True):
        """
        Ranks the character up
        
        Args:
            increment (int, optional): Number of times to rank up. Defaults to 0.
            announce (bool, optional): Print rank up message to console. Defaults to True.
        """
        
        # Store the old values so we can compare them with the new values
        old_rank: int = self.rank
        old_prestige: int = self.prestige
        old_attack: float = self.attack
        old_defence: float = self.defence
        old_health: float = self.health
        health_lost: int = self.max_health - self.health
        
        # Keeps track of total rank in order to scale it
        self.total_rank += increment
        
        self.prestige, self.rank = divmod(self.total_rank, len(CHAR_RANKS))
        
        # Adds 1 to the result because modulo
        self.rank += 1

        if announce:
            
            # If character already had a prestige rank
            if old_prestige > 0:
                print(f"{self.name} has {rc.LIGHT_GREEN}ranked up{rc.END} from {CHAR_RANKS[old_rank]} Prestige {old_prestige} to {CHAR_RANKS[self.rank]} Prestige {self.prestige}!\n")
                sleep(0.2)
                
            elif self.prestige > 0:
                print(f"{self.name} has {rc.LIGHT_GREEN}ranked up{rc.END} from {CHAR_RANKS[old_rank]} to {CHAR_RANKS[self.rank]} Prestige {self.prestige}!\n")
                sleep(0.2)
                
            else:
                print(f"{self.name} has {rc.LIGHT_GREEN}ranked up{rc.END} from {CHAR_RANKS[old_rank]} to {CHAR_RANKS[self.rank]}!\n")
                sleep(0.2)
                
        # Stat scaling
        if self.char_class == "Warrior":
            
            self.attack = self.base_attack + (W_ATK * W_ATK_SCALE ** (self.total_rank - 1))
            self.defence = self.base_defence + (W_DEF * W_DEF_SCALE ** (self.total_rank - 1))
            self.max_health = int(MAX_HEALTH * W_HEALTH_SCALE ** (self.total_rank - 1))

        elif self.char_class == "Tank":

            self.attack = self.base_attack + (T_ATK * T_ATK_SCALE ** (self.total_rank - 1))
            self.defence = self.base_defence + (T_DEF * T_DEF_SCALE ** (self.total_rank - 1))
            self.max_health = int(MAX_HEALTH * T_HEALTH_SCALE ** (self.total_rank - 1))

        elif self.char_class == "Cleric":

            self.attack = self.base_attack + (C_ATK * C_ATK_SCALE ** (self.total_rank - 1))
            self.defence = self.base_defence + (C_DEF * C_DEF_SCALE ** (self.total_rank - 1))
            self.max_health = int(MAX_HEALTH * C_HEALTH_SCALE ** (self.total_rank - 1))
        
        # Adds newly gained health to player health
        self.health = self.max_health - health_lost
        
        # This parameter allows us to quietly level up AI at the start
        if announce:  
            arcade.play_sound(rs.level_up, 1 * rs.volume)
            rm.slow_print(f"\
ATK {rc.LIGHT_RED}{int(old_attack)}{rc.DARK_GRAY} -> {rc.LIGHT_RED}{int(self.attack)}{rc.END} \
DEF {rc.YELLOW}{int(old_defence)}{rc.DARK_GRAY} -> {rc.YELLOW}{int(self.defence)}{rc.END}!", 0.005, 0.2, 0)
            sleep(0.8)

            # Check if the integral health has changed
            if int(old_health) != int(self.health):
                rm.slow_print(f"\
HEALTH {rc.LIGHT_GREEN}{int(old_health)}{rc.DARK_GRAY} -> {rc.LIGHT_GREEN}{int(self.health)}{rc.END}!", 0.005, 0.2, 0)
            
    def experience(self, damage: int, attacker = True, blocked = False):
        """Adds experience and ranks up accordingly

        Args:
            damage (int): Calculates experience based on this value
            attacker (bool, optional): If the unit is the attacker. Defaults to True.
            blocked (bool, optional): If the attack was blocked. Defaults to False.
        """

        def rank_loop():
            """Counts how times we rank up"""
            
            increment = 0
            calculating = True
            
            while calculating:
                
                # Determines our EXP required for next rank
                self.max_exp = int(BASE_MAX_EXP * EXP_SCALING ** (self.total_rank - 1))
                
                # If our exp is higher than our max exp
                if self.exp >= self.max_exp:
                    
                # Consume the required exp to level up then increment the rankup counter
                    self.exp = int(self.exp - self.max_exp)
                    increment += 1
                
                # Finish calculating
                else:
                    calculating = False
                
            # If we've ranked up at least once, call the rank up function
            if increment > 0:
                self.rank_up(increment)
                
        @rm.top_bar
        def add_exp(exp_gain: int):
            """Checks how much experience we get"""
            
            self.exp += exp_gain
            rm.slow_print(f"{self.name} has gained {rc.BROWN}{exp_gain}{rc.END} EXP!")
            rank_loop()
            
            print(f"{self.name} needs {rc.BROWN}{self.max_exp - self.exp}{rc.END} more exp to level up!")
        
        # Prevent dead characters from getting experience
        if self.alive:
            sleep(0.5)
            
            # If we're the one doing damage
            if attacker:
                
                # Get EXP based on damage dealt
                if damage > 0:
                    exp_gain = int(damage)
                    add_exp(exp_gain)
                
                else:
                    rm.slow_print(f"{self.name} has missed!")
            
            # If we're the one receiving damage        
            else:
                if not blocked:
                    # Get 20% more EXP when damage received > 10% max health
                    if damage > 0.1 * self.max_health:
                        exp_gain = int(damage * 1.2)
                        add_exp(exp_gain)
                        
                    # Lecturer wants us to give characters exp based on their damage taken
                    else: 
                        exp_gain = int(damage)
                        add_exp(exp_gain)
                        
                # If attack is blocked
                else:                    
                    
                    # Technically still uses defence stat in order to check
                    # if the attack was blocked to begin with
                    exp_gain = int(damage * 1.5)
                    add_exp(exp_gain)
            
    def stats(self, slow = False):
        """Prints a stat summary of the character according to its state and prestige levels"""
        
        # Concatenates displayed name to 8 characters long
        name = self.name
        if len(name) > 8:
            name = name[:8]

        stat_list = f"\
{rc.LIGHT_WHITE}[ {rc.LIGHT_BLUE}{self.char_class:^7}{rc.END} \
{name:^8} >  \
{rc.DARK_GRAY}HP: {rc.LIGHT_GREEN}{int(self.health):>5}{rc.DARK_GRAY}/{int(self.max_health):<5}{rc.END} \
{rc.DARK_GRAY}ATTACK: {rc.LIGHT_RED}{int(self.attack):<5}{rc.END} \
{rc.DARK_GRAY}DEFENCE: {rc.LIGHT_CYAN}{int(self.defence):<5}{rc.END} \
{rc.DARK_GRAY}EXP: {rc.BROWN}{self.exp:>4}/{self.max_exp:<4}{rc.END} \
{rc.DARK_GRAY}PSN: {rc.LIGHT_PURPLE}{self.poisoned:<2}{rc.END} \
{rc.DARK_GRAY}SHIELD: {rc.LIGHT_GREEN}{self.shielded:<1}{rc.END} \
{rc.DARK_GRAY}RANK: {CHAR_RANKS[self.rank]:<11}"

        if self.prestige == 0:
            if slow:
                rm.slow_print(stat_list, 0.001, 0.4, 0, 0.8)
            else:
                print(stat_list)
        else:
            if slow:
                rm.slow_print(f"{stat_list} {rc.DARK_GRAY}{rc.LIGHT_WHITE}{self.prestige}{rc.END}", 0.001, 0.4, 0, 0.8)
            else:
                print(f"{stat_list} {rc.DARK_GRAY}{rc.LIGHT_WHITE}{self.prestige}")

    def death_check(self):
        """Updates character's alive status based on their health"""
        
        if self.health <= 0:
            self.health = 0
            self.alive = False
        
        elif self.health >= 0:
            self.alive = True
        
    # Combat
#                            ___
#                           ( ((
#                            ) ))
#   .::.                    / /(
#  'M .-;-.-.-.-.-.-.-.-.-/| ((::::::::::::::::::::::::::::::::::::::::::::::.._
# (J ( ( ( ( ( ( ( ( ( ( ( |  ))   -====================================-      _.>
#  `P `-;-`-`-`-`-`-`-`-`-\| ((::::::::::::::::::::::::::::::::::::::::::::::''
#   `::'                    \ \(
#                            ) ))
#                           (_((

    def crit(self, damage: int, chance = CRIT_CHANCE):
        """Call this before calculating final damage for moves that can crit

        Args:
            damage (int): Damage before crit
            chance (int): Chance to crit. Defaults to CRIT_CHANCE

        Returns:
            bool: Whether the attack crit, int: Damage after checking for crit
        """
        
        if random.randrange(chance) == 0:
            damage *= CRIT_MULTIPLIER
            return True, int(damage)
        
        #If crit fails, no change to damage value
        else:
            return False, int(damage)

    def do_damage(self,
                  damage: int, 
                  target: object, 
                  target_defence: int,
                  sound_count: int = 1, 
                  sound_effect = rs.sword_attack,
                  volume: float = 0.8 * rs.volume
                  ):
        """Does basic damage calculation against another unit

        Args:
            damage (int): How much damage we're trying to deal
            target_health (object): The target object
            sound_count (int, optional): Number of times to play attack sound. Defaults to 1.
            sound_effect (object, optional): Attack sound. Defaults to rs.sword_attack.
            volume (float, optional): Volume of the sound. Defaults to 0.8 * rs.volume.

        Returns:
            tuple: Final damage (int), Target remaining health (float)
            
        This one is weird because I wrote it when I was still a noob at objects
        """
        
        final_damage = damage - target_defence
        
        # If character is shielded, block 75% damage
        if target.shielded:
            final_damage /= 4
            arcade.play_sound(rs.shield_broken)
            print(f"{target.name}'s shield reduces the next attack to {rc.LIGHT_RED}{int(final_damage)}{rc.END} damage!")
            sleep(0.2)
            target.shielded = False
        
        # If character is cloaked, 50% chance to nullify damage
        # Damage has to be more than 0 because this was a last-minute addition and I need to pass the block check later on
        if target.cloaked:
            if random.randrange(2) == 0:
                if final_damage > 10:
                    final_damage = random.randrange(1, 10)
                else:
                    final_damage = 1
                
                arcade.play_sound(rs.cloak_miss)
                print(f"{target.name} set up a decoy for {rc.LIGHT_GREEN}{final_damage}{rc.END} health!")
                sleep(0.2)
            
            print(f"{rc.DARK_GRAY}{target.name} has been uncloaked!{rc.END}")
            target.cloaked = False
        
        updated_target_health = target.health - final_damage
        
        if final_damage > 0:
            for _ in range(sound_count):
                arcade.play_sound(sound_effect, volume)
                sleep(0.25)
            
            # Prevents overkill attacks which break exp calculation
            if updated_target_health < 0:
                final_damage = target.health
                updated_target_health = 0
        
        # If damage was blocked
        elif final_damage <= 0:
            arcade.play_sound(sound_effect, 0.5 * volume)
            final_damage = 0
            updated_target_health = target.health
            
        return int(final_damage), int(updated_target_health)
    
    def attack_results(self, final_damage: int, damage: int, target: object):
        """Updates experience and states of all involved characters

        Args:
            final_damage (int): Final damage dealt
            damage (int): Initial attempted damage
            target (object): Target unit
        """
    
        def attack_success(attacker: object, target: object, final_damage: int):
            """Final calculations for a successful attack"""
            
            rm.slow_print(f"\n{target.name} received {rc.LIGHT_RED}{int(final_damage)}{rc.END} damage!")            
            rm.slow_print(f"{target.name} remaining health: {rc.LIGHT_GREEN}{int(target.health)}{rc.DARK_GRAY}/{int(target.max_health)}{rc.END}")
        
            attacker.experience(final_damage)
            target.death_check()
            target.experience(target.defence, False)
            
        def attack_blocked(target: object, damage: int):
            """Final calculations for a blocked attack"""
            
            rm.slow_print(f"{target.name} blocked {rc.LIGHT_RED}{damage}{rc.END} damage!")
            target.experience(damage, False, True)

        # Check which function to run
        if final_damage > 0 or damage == 0:
            attack_success(self, target, final_damage)
 
        else:
            attack_blocked(target, int(damage))

    def heal(self, healer: object, target: object, heal_strength: float):
        """Heals a friendly unit

        Args:
            healer (object): Character doing the healing
            target (object): Character receiving
            heal_strength (float): Multiply heal strength
        """
        
        missing_health = target.max_health - target.health
        
        # If healing self, heal strength is 200% attack
        if healer is target:
            healing = int(healer.attack * 2)
        
        # Else, healing is based off the healer's attack and the heal strength of the move
        else:
            healing = int(healer.attack * heal_strength)
            
        # Prevents overhealing/displaying a huge heal number
        if healing > missing_health:
            healing = missing_health
        
        # Adds the final healing amount to the target health
        target.health += healing
        
        # Checks if target has been revived
        if not target.alive:
            arcade.play_sound(rs.revive)
            sleep(0.2)
            rm.slow_print(f"{rc.LIGHT_GREEN}{target.name}{rc.LIGHT_WHITE} has been revived!{rc.END}")
            sleep(0.5)
        
        # Updates target's alive status   
        target.death_check()
        
        if healing != 0:
            rm.slow_print(f"{rc.LIGHT_GREEN}{target.name}{rc.DARK_GRAY} has been healed for {rc.LIGHT_GREEN}{int(healing)}{rc.END}!")
            rm.slow_print(f"{rc.LIGHT_GREEN}{target.name}{rc.DARK_GRAY} now has {rc.LIGHT_GREEN}{int(target.health)}/{int(target.max_health)}{rc.END} health")
        
        else:
            rm.slow_print(f"{target.name} is already at full health!")
    
    def BasicAttack(self, target: object):
        """Basic attack given to everyone that deals damage according to the task sheet

        Args:
            target (object): Target to attack

        Returns:
            tuple: hostile (bool), aoe (bool)\n
            Checks if the move is hostile, aoe, or both
        """
        
        attack_sound = rs.sword_attack
        damage_range = (-5, 10)
        
        hostile = True
        aoe = False
        
        # This is necessary in order to let it return hostile, aoe values before actually running
        if target:
            
            # This randomises the damage a bit according to the task
            damage = self.attack + random.randint(*damage_range)
            
            # In case damage is negative because Tanks can hit negative with this damage range
            if damage < 0:
                damage = 0
            
            crit_success, damage = self.crit(damage)
            
            # Change our attack sound if crit
            if crit_success:
                attack_sound = rs.dagger_attack
                
            # 5% chance to miss
            if random.randrange(20) == 0:
                damage = 0
            
            final_damage, target.health = self.do_damage(damage, target, target.defence, sound_effect = attack_sound)
            rm.slow_print(f"{self.name} hits {target.name} with {rc.LIGHT_RED}{damage}{rc.END} damage!")
            
            if crit_success:
                rm.slow_print(f"{rc.YELLOW}Critical {rc.LIGHT_WHITE}hit!{rc.END}")
                sleep(0.8)
            
            self.attack_results(final_damage, damage, target)

        return hostile, aoe
    
# Subclasses

# ,_._._._._._._._._|__________________________________________________________,
# |_|_|_|_|_|_|_|_|_|_________________________________________________________/
#                   !

class Warrior(unit):
    """Balanced character with moderate attack and defence stats\n
    :param Str name: Name of the character
    :param Str team: Team the character belongs to (Players/AIs)"""
    
    def __init__(self, name, team):
        super().__init__(name, team)
        self.char_class = "Warrior"
        self.attack, self.defence = random.randint(*W_BASE_ATK), random.randint(*W_BASE_DEF)
        self.base_attack, self.base_defence = self.attack, self.defence
        
        # Character movelist
        self.movelist.update(
                             {2: self.DaggerSpray,
                             3: self.Neutralise,
                             4: self.Rage,
                             5: self.Execute,
                             6: self.Sweep}
                             )
        
    def DaggerSpray(self: object, target: object):
        """Single target attack that hits 3-5 times for 30% damage each, then cloaks"""
    
        attack_sound = rs.dagger_attack
        
        hostile = True
        aoe = False
        
        # This is necessary in order to let it return hostile, aoe values before actually running
        if target:
            hit_count = random.randint(3, 5)
            
            damage = (self.attack * 0.3) * hit_count
            crit_success, damage = self.crit(damage)
            
            # Change our attack sound if crit
            if crit_success:
                attack_sound = rs.dagger_attack
            
            final_damage, target.health = self.do_damage(damage, target, target.defence, hit_count, attack_sound, 1.2)
            rm.slow_print(f"Hit {hit_count} times for {rc.LIGHT_RED}{int(damage)}{rc.END} total damage!")
            
            # I KNOW I'M REPEATING CODE THIS WAS A LAST MINUTE ADDITION SORRY
            if crit_success:
                rm.slow_print(f"{rc.YELLOW}Critical {rc.LIGHT_WHITE}hit!{rc.END}")
                sleep(0.8)
                
            print(f"{rc.LIGHT_GREEN}{self.name}{rc.DARK_GRAY} has retreated into the shadows...{rc.END} ")
            
            # Checks the results of our attack
            self.attack_results(final_damage, damage, target)
            
            self.cloaked = True
            
        return hostile, aoe
   
    def Neutralise(self: object, target: object):
        """Armour-piercing attack that ignores 50% defence but does 90% damage"""

        attack_sound = rs.sword_attack
        
        hostile = True
        aoe = False

        if target:
            
            damage = self.attack * 0.9
            crit_success, damage = self.crit(damage)
            
            # Change our attack sound if crit
            if crit_success:
                attack_sound = rs.dagger_attack
            
            final_damage, target.health = self.do_damage(damage, target, int(target.defence / 2), 1, attack_sound, 1.2)
            rm.slow_print(f"Neutralising {target.name} with {rc.LIGHT_RED}{int(damage)}{rc.END} damage!")
            
            # I KNOW I'M REPEATING CODE THIS WAS A LAST MINUTE ADDITION SORRY
            if crit_success:
                rm.slow_print(f"{rc.YELLOW}Critical {rc.LIGHT_WHITE}hit!{rc.END}")
                sleep(0.8)
                
            # Checks the results of our attack
            self.attack_results(final_damage, damage, target)
        
        return hostile, aoe
    
    def Rage(self: object, target: object):
        """Sacrifice 10% health to do double damage"""

        attack_sound = rs.rage
        
        hostile = True
        aoe = False

        if target:
            
            damage = self.attack * 2
            crit_success, damage = self.crit(damage)
            
            final_damage, target.health = self.do_damage(damage, target, target.defence, 1, attack_sound, 0.8)
            rm.slow_print(f"Consumed {rc.LIGHT_GREEN}{int(self.health * 0.1)}{rc.DARK_GRAY}/{int(self.health)}{rc.END} health and dealt {rc.LIGHT_RED}{int(damage)}{rc.END} damage to {target.name}!")
            self.health = int(self.health * 0.9)
            
            # I KNOW I'M REPEATING CODE THIS WAS A LAST MINUTE ADDITION SORRY
            if crit_success:
                rm.slow_print(f"{rc.YELLOW}Critical {rc.LIGHT_WHITE}hit!{rc.END}")
                sleep(0.8)
                
            # Checks the results of our attack
            self.attack_results(final_damage, damage, target)
        
        return hostile, aoe
    
    def Execute(self: object, target: object):
        """Deals more damage the lower the enemy health is.\n
        This attack cannot crit."""

        attack_sound = rs.execute
        
        hostile = True
        aoe = False

        if target:
            
            damage = self.attack * (0.4 * target.max_health / target.health)
            
            final_damage, target.health = self.do_damage(damage, target, target.defence, 1, attack_sound, 0.8)
            rm.slow_print(f"{rc.DARK_GRAY}Executing{rc.END} {target.name} with {rc.LIGHT_RED}{int(damage)}{rc.END} damage!")
                
            # Checks the results of our attack
            self.attack_results(final_damage, damage, target)
        
        return hostile, aoe
    
    def Sweep(self: object, target: object):
        """Leg sweep all enemies and deal damage based on their defence\n
        This attack cannot crit."""
        
        attack_sound = rs.kick
        
        hostile = True
        aoe = True
        
        if target:
            
            damage = target.defence + self.attack * 0.5
            
            final_damage, target.health = self.do_damage(damage, target, target.defence, 1, attack_sound, 1.2)
            rm.slow_print(f"Swept {target.name} for {rc.LIGHT_RED}{int(damage)}{rc.END} damage!")

            # Checks the results of our attack
            self.attack_results(final_damage, damage, target)
            
        return hostile, aoe

class Tank(unit):
    """Magic-based character with high attack and low defence stats\n
    :param Str name: Name of the character
    :param Str team: Team the character belongs to (Players/AIs)"""
    
    def __init__(self, name, team):
        super().__init__(name, team)
        self.char_class = "Tank"
        
        # Randomises initial stats
        self.attack, self.defence = random.randint(*T_BASE_ATK), random.randint(*T_BASE_DEF)
        
        # Saves the base stats for future calculations
        self.base_attack, self.base_defence = self.attack, self.defence
        self.movelist.update(
                        {2: self.Equaliser,
                        3: self.RecklessCharge,
                        4: self.Barricade}
                        )
    

    def Equaliser(self, target: object):
        """Deals damage based on the difference between the character's attack and the enemy's defence. \n
        This attack cannot crit and is weak if the difference is small"""
        
        attack_sound = rs.break_attack
        
        hostile = True
        aoe = False

        if target:
            
            # Gets the difference regardless of whether it's positive or negative
            damage = abs(self.attack - target.defence) * 5
            
            # Remove target defence from calculation
            final_damage, target.health = self.do_damage(damage, target, 0, 1, attack_sound, 1)
            rm.slow_print(f"Equalised {target.name} with {rc.LIGHT_RED}{int(damage)}{rc.END} damage!")
            
            # Checks the results of our attack
            self.attack_results(final_damage, damage, target)
        
        return hostile, aoe
    
    def RecklessCharge(self, target: object):
        """A risky but powerful attack that has a 20% chance to miss"""
        
        attack_sound = rs.break_attack
        
        hostile = True
        aoe = False
        
        if target:
            
            # 1/5 chance to miss
            miss = random.randrange(5)
            
            if miss != 0:
                damage = self.attack * 3
                
                # Calculate crit
                crit_success, damage = self.crit(damage)
                    
                final_damage, target.health = self.do_damage(damage, target, target.defence, 1, attack_sound, 1)
                rm.slow_print(f"Charged {target.name} with {rc.LIGHT_RED}{int(damage)}{rc.END} damage!")
                
                # I KNOW I'M REPEATING CODE THIS WAS A LAST MINUTE ADDITION SORRY
                if crit_success:
                    rm.slow_print(f"{rc.YELLOW}Critical {rc.LIGHT_WHITE}hit!{rc.END}")
                    sleep(0.8)
                    
                # Checks the results of our attack
                self.attack_results(final_damage, damage, target)
            
            else:
                rm.slow_print(f"{self.name} has missed!")
        
        return hostile, aoe
    
    def Barricade(self, target: object):
        """Gives all allies the shielded state for damage reduction"""
        
        hostile = False
        aoe = True
        
        if target:
            if target.alive:    
                target.shielded = True
                arcade.play_sound(rs.shield, 0.6)
                rm.slow_print(f"Shielded {rc.LIGHT_GREEN}{target.name}{rc.END}!")
                sleep(0.4)
            
        return hostile, aoe
            
class Cleric(unit):
    """Magic-based character with high attack and low defence stats\n
    :param Str name: Name of the character
    :param Str team: Team the character belongs to (Players/AIs)"""
    
    def __init__(self, name, team):
        super().__init__(name, team)
        self.char_class = "Cleric"
        self.attack, self.defence = random.randint(*C_BASE_ATK), random.randint(*C_BASE_DEF)
        self.base_attack, self.base_defence = self.attack, self.defence
        self.movelist.update(
                        {2: self.Lightning,
                        3: self.Restoration,
                        4: self.Curse,
                        5: self.PoisonCloud}
                        )

    def Lightning(self, target: object):
        """Moderate lightning spell that hits all targets with 85% damage.\n
        This attack cannot crit."""
        
        hostile = True
        aoe = True
        
        if target:
            
            damage = (self.attack * 0.85)
            
            final_damage, target.health = self.do_damage(damage, target, target.defence, 1, rs.thunder_attack, 0.5)
            print(f"Cast a {rc.YELLOW}lightning bolt{rc.END} on {target.name} for {rc.LIGHT_RED}{int(damage)}{rc.END} damage!")
            
            self.attack_results(final_damage, damage, target)
        
        return hostile, aoe
    
    def Restoration(self, target: object):
        """Heals and revives an ally with magic."""
        
        hostile = False
        aoe = False
        
        # Randomise the heal strength a bit
        heal_strength = random.uniform(0.9, 1.5)
        
        if target:
                        
            self.heal(self, target, heal_strength)
        
        return hostile, aoe
    
    def Curse(self, target: object):
        """Deals damage based on the enemy's attack.\n
        This attack cannot crit."""
        
        attack_sound = rs.curse
        
        hostile = True
        aoe = False
        
        if target:
            
            damage = (target.attack/self.attack * 10) + self.attack
            
            final_damage, target.health = self.do_damage(damage, target, target.defence, 1, attack_sound, 0.8)
            print(f"Cursed {target.name} for {rc.LIGHT_RED}{int(damage)}{rc.END} damage!")
            
            self.attack_results(final_damage, damage, target)
        
        return hostile, aoe
    
    def PoisonCloud(self, target: object):
        """Poisons all enemies for 2 rounds."""

        hostile = True
        aoe = True
        
        if target:
            arcade.play_sound(rs.poison)
            target.poisoned += 2
            print(f"{rc.LIGHT_RED}{target.name}{rc.END} is now{rc.LIGHT_PURPLE} poisoned {rc.END}for {rc.LIGHT_PURPLE}{target.poisoned}{rc.END} rounds!")
            sleep(0.6)
        
        return hostile, aoe

# 13/11/2023: Learned classes could go into lists a bit too late
# classes = [unit.Warrior, unit.Tank, unit.Cleric
# Should've random.choice(classes)'d this