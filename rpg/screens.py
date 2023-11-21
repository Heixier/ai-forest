import rpg_colours as rc
import rpg_modules as rm

def game_help():
    """Prints game help"""
    
    print(f"\n\
{rc.LIGHT_WHITE}HELP MENU{rc.END}\n\n\
{rc.LIGHT_RED}attack/a{rc.DARK_GRAY} - {rc.END}choose attack\n\
{rc.LIGHT_BLUE}auto{rc.DARK_GRAY} - {rc.END}automatically attack\n\
{rc.BROWN}stats{rc.DARK_GRAY} - {rc.END}displays stats\n\
{rc.LIGHT_WHITE}movelist{rc.DARK_GRAY} - {rc.END}show movelist\n\
{rc.LIGHT_GREEN}help{rc.DARK_GRAY} - {rc.END}displays this screen\
")
    
def forest():
    """
    Prints a house in the forest\n
    Colour design by Ansar
    """
    
    rm.line_print(length = 60)
    
    rm.slow_print(f"\n\
     {rc.GREEN}^  ^  ^   ^  {rc.END}  {rc.LIGHT_RED}    ___I_     {rc.GREEN} ^  ^   ^  ^  ^   ^  ^\n\
    /|\/|\/|\ /|\  {rc.END}  {rc.LIGHT_RED}  /\-_--\    {rc.GREEN}/|\/|\ /|\/|\/|\ /|\/|\\\n\
    /|\/|\/|\ /|\  {rc.END} {rc.LIGHT_RED}  /  \_-__\   {rc.GREEN}/|\/|\ /|\/|\/|\ /|\/|\\\n\
    /|\/|\/|\ /|\  {rc.END} {rc.LIGHT_RED}  |{rc.RED}[]{rc.LIGHT_RED}| {rc.RED}[] {rc.LIGHT_RED}|  {rc.GREEN} /|\/|\ /|\/|\/|\ /|\/|\\\n\n\
                  {rc.YELLOW}{rc.BOLD}    RPG GAME{rc.END}\n\
             {rc.LIGHT_WHITE}{rc.FAINT} (Role-Playing game game){rc.END}", speed = 0.003, delay = 0.5, sound = False)
    
    rm.line_print(length = 60)
    
def alt_forest():
    """Prints a house in the forest"""
    
    rm.line_print(length = 60)
    
    rm.slow_print(f"\n\
     {rc.DARK_GRAY}^  ^  ^   ^        ___I_      ^  ^   ^  ^  ^   ^  ^\n\
    /|\/|\/|\ /|\      /\-_--\    /|\/|\ /|\/|\/|\ /|\/|\\\n\
    /|\/|\/|\ /|\     /  \_-__\   /|\/|\ /|\/|\/|\ /|\/|\\\n\
    /|\/|\/|\ /|\     |[]| [] |   /|\/|\ /|\/|\/|\ /|\/|\\\n\n\
                      RPG GAME\n\
              (Role-Playing game game){rc.END}", speed = 0.003, delay = 0.5, sound = False)
    
    rm.line_print(length = 60)