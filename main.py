import numpy as np
from time import sleep
import pygame
import os
import pygame_menu
from GUIext import *
from rand import randint

TIME = 1.0

RATIO = (1, 1) # Frozen for button squareness
HEIGHT = 720
WIDTH = HEIGHT//RATIO[0]*RATIO[1]

BLUE = (0, 0, 0)
WHITE = (255, 255, 255)

BUTTON_HEIGHT = HEIGHT//3
BUTTON_WIDTH = WIDTH//3

PLAYER_1 = 1
PLAYER_2 = 2

ITERS = 0

game_grid = [[None]*3 for _ in range(3)]

one_player = False
difficult = False

def start():
    global one_player, difficult
    one_player = player_selector.get_value()[0][1]
    difficult = difficult_selector.get_value()[0][1]
    print(one_player)
    menu.disable()
    
def grid_full():
    return ITERS >= 9

def win(r, c, player):
    if game_grid[r].count(player) == 3:
        print("Line wins!")
        return True
    
    for line in game_grid:
        if line[c] != player:
            break
    else:
        print("Column wins!")
        return True
        
    if game_grid[0][0] != None and game_grid[0][0] == game_grid[1][1] == game_grid[2][2]:
        print("Diag wins!")
        return True
    if game_grid[0][2] != None and game_grid[0][2] == game_grid[1][1] == game_grid[2][0]:
        print("Diag wins!")
        return True
    return False

### Counts clones from (r,c) towards a given direction (dv, dh)
def count_from_towards(r, c, dr, dc, player):
    n = 1
    r+=dr
    c+=dc  
    while 0<=r<=2 and 0<=c<=2 and game_grid[r][c] == player:
        n+=1
        r+=dr
        c+=dc 
    return n

### Counts maximum from (r, c), covering all directions
def count_from(r, c, player):
    maximum = count_from_towards(r, c, 1, 0, player) + count_from_towards(r, c, -1, 0, player)-1
    maximum = max(maximum, count_from_towards(r, c, 0, 1, player) + count_from_towards(r, c, 0, -1, player)-1)
    maximum = max(maximum, count_from_towards(r, c, 1, 1, player) + count_from_towards(r, c, -1, -1, player)-1)
    maximum = max(maximum, count_from_towards(r, c, -1, 1, player) + count_from_towards(r, c, 1, -1, player)-1)
    return maximum

WIN = 4 # Superior score

def best_fit(r, c):
    max_count_from_1 = count_from(r, c, PLAYER_1)
    max_count_from_2 = count_from(r, c, PLAYER_2)
    if max_count_from_2 >= 3:
        return WIN
    return max(max_count_from_1, max_count_from_2)

def move():
    nones = [(r, c) for r, row in enumerate(game_grid) for c, val in enumerate(row) if val == None]

    l = sorted(nones, key=lambda pos: best_fit(*pos))
    print(l)
    return l[-1]


def grid(blck_height = BUTTON_HEIGHT, blck_width = BUTTON_WIDTH):
    for y in range(0, HEIGHT, blck_width):
        for x in range(0, WIDTH, blck_height):
            # pygame.draw.rect(screen, BLUE, rect, 1)
            yield Button(pygame.Rect(x, y, blck_width, blck_height))

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

menu = pygame_menu.Menu(title="Bienvenue", width=WIDTH, height=HEIGHT, theme=pygame_menu.themes.THEME_DARK)
player_selector = menu.add.selector(title="Nombre joueurs: ", items=[("1", True), ("2", False)])
difficult_selector = menu.add.selector(title="Difficulté: ", items=[("Facile", False), ("Difficile", True)])
menu.add.button('Start', start)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(SCREEN)

SCREEN.fill(WHITE)

exe_dir = os.path.dirname(os.path.abspath(__file__))
cross_img = pygame.transform.scale(pygame.image.load(os.path.join(exe_dir, "images", "cross.png")), (BUTTON_WIDTH, BUTTON_HEIGHT))
circle_img = pygame.transform.scale(pygame.image.load(os.path.join(exe_dir, "images", "circle.png")), (BUTTON_WIDTH, BUTTON_HEIGHT))

buttons = np.array(list(grid())).reshape((3, 3))
gen = iter(buttons.flatten()) # will be constantly emptied and refilled for grid displaying

player = PLAYER_1
player_mapping = {PLAYER_1: cross_img, PLAYER_2: circle_img}
running = True
r = c = 0
vol_quit = False

while running:
    try:
        pygame.draw.rect(SCREEN, BLUE, next(gen), 1)
    except StopIteration:
        gen = iter(buttons.flatten())
    pygame.display.update()

    # Row and column getting
    if player == PLAYER_2 and one_player:
        r, c = move() if difficult else 
        sleep(TIME)
    else:
        if pygame.event.peek(eventtype=QUIT):
            vol_quit = True
            break
        if not pygame.event.peek(eventtype=MOUSEBUTTONDOWN):
            continue
        #Mouse button was clicked
        r, c = clicked_on_who(*pygame.mouse.get_pos(), buttons)
        pygame.event.clear()
    ITERS+=1
    if not buttons[r][c].is_clickable():
        continue
    game_grid[r][c] = player
    buttons[r][c].add_image(player_mapping[player], SCREEN)
    buttons[r][c].clickable = False
    
    if win(r, c, player):
        print(f"Player {player} wins!")
        break
    if grid_full():
        print(f"Game grid is full!")
        break
    
    player = PLAYER_2 if player == PLAYER_1 else PLAYER_1

if not vol_quit:
    print("Click anywhere to quit!")
    while not pygame.event.peek(eventtype=MOUSEBUTTONDOWN):
        pygame.display.update()
pygame.quit()
