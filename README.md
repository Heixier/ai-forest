# The Rainforest
A simple text-based game with various character classes and strategic gameplay.  
Your goal is to clear as many stages as possible.

## Installation notes

Please do not run in Python versions higher than 3.11.6 when installing arcade!  
<sub>(arcade 23.3.1 (latest) only supports Pillow 9.3.0 which only supports up to Python 3.11.6)</sub>  
  
#### Recommended Python version:

**3.11.6**  
[Link to Python 3.11.6](https://www.python.org/downloads/release/python-3116/)

### Install arcade
To install arcade, enter this into your command line:

```
pip3 install arcade
```

## Getting started

In order to get the game:  

Click on the code button on the top right and download the ZIP

Then run the main game launcher in ```rpg/console/rpg_main.py``` with Python
## How to play

The game is mostly controlled by entering numbers to select from the displayed options

For questions, the default responses are:  
Yes:
```yes``` or ```y```  
No:
```no``` or ```n```

## Movelist

```Basic Attack```
Medium base damage attack

### Warrior

```DaggerSpray```  
Launch a flurry of 3-5 knives and cloak yourself for a 50% chance to significantly reduce the damage of the next received attack

```Neutralise```  
Armour-piercing attack that ignores half of the enemy's defence for slightly lower base damage

```Rage```  
Sacrifice a portion of your health to deal increased damage

```Execute```  
Deals more damage the lower the enemy health is.  
This attack cannot crit.

```Sweep```  
Leg sweep all enemies and deal damage based on their defence.  
This attack cannot crit.

### Tank

```Equaliser```  
Deals damage based on the difference between attack and enemy defence stat  
(This attack cannot crit)

```Reckless charge```  
High damage attack with a 20% chance to miss

```Barricade```  
Gives all allies the shielded state for 75% damage reduction on their next received attack

### Cleric

```Lightning```  
Strike all enemies with a medium damage lightning bolt  
(This attack cannot crit)

```Restoration```  
Heal and revive a single ally (bonus healing when used on self)  

```Curse```  
Uses the enemy's own attack to deal damage.  
This attack cannot crit.

```PoisonCloud```  
Poisons all enemies for 2 rounds

## Sound credits
Pixabay for most of the sound effects  
  
More sound effects from:  
Diablo II, For Honor, Sekiro, COD Warzone