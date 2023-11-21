import rpg_colours as rc

def gamelog():
    print(f"{rc.LIGHT_WHITE}GAMELOG START{rc.END}\n")

    try:
        with open("gamelog.txt", "r") as f:
            for line in f:
                print(line, end = "")
                
    except FileNotFoundError:
        print("ERROR: File not found.")

    except:
        print("ERROR: File may be corrupted.")
        
    print(f"{rc.LIGHT_WHITE}\nGAMELOG END{rc.END}\n")
    
    input(f"{rc.DARK_GRAY}Press Enter to exit. {rc.END}")

# Prevent this script from automatically running when imported into other files
if __name__ == "__main__":
    gamelog()