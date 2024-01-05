import numpy as np
import pygame
import argparse
from GUIext import *

RATIO = (1, 1) # Frozen for button squareness
HEIGHT = 720
WIDTH = HEIGHT//RATIO[0]*RATIO[1]

BLUE = (0, 0, 255)
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
    return sorted(nones, key=lambda pos: count_from(pos[0], pos[1], PLAYER_1))[-1], sorted(nones, key=lambda pos: count_from(pos[0], pos[1], PLAYER_2))[-1]
    
            
def grid(blck_height = BUTTON_HEIGHT, blck_width = BUTTON_WIDTH):
    for y in range(0, HEIGHT, blck_width):
        for x in range(0, WIDTH, blck_height):
            # pygame.draw.rect(screen, BLUE, rect, 1)
            yield Button(pygame.Rect(x, y, blck_width, blck_height))

parser = argparse.ArgumentParser()
parser.add_argument('--robot', action="store_true")
one_player = parser.parse_args().robot # Get "robot" argument

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
SCREEN.fill(WHITE)

cross_img = pygame.transform.scale(pygame.image.load("cross.png"), (BUTTON_WIDTH, BUTTON_HEIGHT))
circle_img = pygame.transform.scale(pygame.image.load("circle.png"), (BUTTON_WIDTH, BUTTON_HEIGHT))

buttons = np.array(list(grid())).reshape((3, 3))
gen = iter(buttons.flatten())

player = PLAYER_1
player_mapping = {PLAYER_1: cross_img, PLAYER_2: circle_img}

while True:
    event = pygame.event.wait()
    if event.type == MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        print("Clicked!")
        r, c = clicked_on_who(mouse_x, mouse_y, buttons)
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
        print(best_fit())
        ITERS+=1

    try:
        pygame.draw.rect(SCREEN, BLUE, next(gen), 1)
    except StopIteration:
        gen = iter(buttons.flatten())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

pygame.quit()