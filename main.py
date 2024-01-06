import numpy as np
import os
import pygame
from GUIext import *

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
winners = {PLAYER_1: [], PLAYER_2: []}

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

def count_from_towards(r, c, dh, dv, player):
    n = 1
    r+=dv
    c+=dh  
    while 0<=r<=2 and 0<=c<=2:
        if game_grid[r][c] == player:
            n+=1
        else:
            break
        r+=dv
        c+=dh  
    return n

def count_from(r, c, player):
    maximum = count_from_towards(r, c, 1, 0, player) + count_from_towards(r, c, -1, 0, player)-1
    maximum = max(maximum, count_from_towards(r, c, 0, 1, player) + count_from_towards(r, c, 0, -1, player)-1)
    maximum = max(maximum, count_from_towards(r, c, 1, 1, player) + count_from_towards(r, c, -1, -1, player)-1)
    return maximum

def best_fit():
    nones = [(r, c) for r, row in enumerate(game_grid) for c, val in enumerate(row) if val == None]
    player_one_best = sorted(nones, key=lambda pos: count_from(pos[0], pos[1], PLAYER_1))[-1]
    player_two_best = sorted(nones, key=lambda pos: count_from(pos[0], pos[1], PLAYER_2))[-1]
    return player_one_best if count_from(*player_one_best, PLAYER_1) >= count_from(*player_two_best, PLAYER_2) else player_two_best
    
def grid(blck_height = BUTTON_HEIGHT, blck_width = BUTTON_WIDTH):
    for y in range(0, HEIGHT, blck_width):
        for x in range(0, WIDTH, blck_height):
            # pygame.draw.rect(screen, BLUE, rect, 1)
            yield Button(pygame.Rect(x, y, blck_width, blck_height))
players_n = 0
while players_n not in [1, 2]:
    players_n = int(input("Nombre joueurs(1/2): "))
one_player = players_n == 1

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
SCREEN.fill(WHITE)

exe_dir = os.path.dirname(os.path.abspath(__file__))
os.path.join(exe_dir, "images", "cross.png")
# images root is used by PyInstaller when bundling images into the executable
cross_img = pygame.transform.scale(pygame.image.load(os.path.join(exe_dir, "images", "cross.png")), (BUTTON_WIDTH, BUTTON_HEIGHT))
circle_img = pygame.transform.scale(pygame.image.load(os.path.join(exe_dir, "images", "circle.png")), (BUTTON_WIDTH, BUTTON_HEIGHT))

buttons = np.array(list(grid())).reshape((3, 3))
gen = iter(buttons.flatten())

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
        r, c = best_fit()
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
