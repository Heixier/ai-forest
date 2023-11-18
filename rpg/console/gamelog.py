# Run this file to print gamelog

print("GAMELOG START\n")
with open("gamelog.txt", "r") as f:
    for line in f:
        print(line)

print("GAMELOG END")