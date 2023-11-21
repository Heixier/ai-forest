import arcade

volume = 1

# Background
bgm = arcade.load_sound("sounds/rain.mp3", streaming = True)
intro = arcade.load_sound("sounds/storm.wav")

# General game effects
text = arcade.load_sound("sounds/text.mp3")
text_2 = arcade.load_sound("sounds/boom.wav")
auto = arcade.load_sound("sounds/AutoMode.mp3")
ready = arcade.load_sound("sounds/SwordReady.wav")

# Game states
start = arcade.load_sound(":resources:sounds/upgrade4.wav") # please change this
lose = arcade.load_sound(":resources:sounds/explosion1.wav")

win = arcade.load_sound(":resources:sounds/coin1.wav")

# Character states
# death = arcade.load_sound("sounds/oof.mp4")
death = arcade.load_sound("sounds/GroundDrop.mp3")
revive = arcade.load_sound("sounds/Choir.wav")
level_up = arcade.load_sound("sounds/levelup2.mp3")

# Character effects
hit = arcade.load_sound("sounds/stab.wav")
block = arcade.load_sound("sounds/block.wav")
shield_broken = arcade.load_sound("sounds/ShieldBroken.wav") # COD Warzone
cloak_miss = arcade.load_sound("sounds/whoosh.mp3")

# Character attacks
sword_attack = arcade.load_sound("sounds/SwordAttack.mp3")
dagger_attack = arcade.load_sound("sounds/DaggerAttack.mp3")
execute = arcade.load_sound("sounds/Slash1.wav")
rage = arcade.load_sound("sounds/valhalla.wav") # For Honor
curse = arcade.load_sound("sounds/Curse.wav")
kick = arcade.load_sound("sounds/kick.mp3")
thunder_attack = arcade.load_sound("sounds/thunder.wav")
break_attack = arcade.load_sound("sounds/BreakAttack.mp3")
nuke_attack = arcade.load_sound("sounds/HeavyBoom.wav")

# Character buffs/debuffs
heal = arcade.load_sound("sounds/Harp.wav")
shield = arcade.load_sound("sounds/shield.wav") # Sekiro
poison = arcade.load_sound("sounds/potion.wav") # Diablo II