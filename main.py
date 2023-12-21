import numpy as np
import pygame
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

game_grid = [[None]*3]*3
winners = {PLAYER_1: [], PLAYER_2: []}

def grid_full():
    return ITERS >= 9

def win(r, c, player):
    if game_grid.count(player) == 3:
        return True
    for line in game_grid:
        if line[0] != player:
            break
    else:
        return True
    if game_grid[0][0] == game_grid[1][1] == game_grid[2][2]:
        return True
    return False

def finished(r, c, player):
    return win(r, c, player) or grid_full()

def grid(blck_height = HEIGHT//3, blck_width = WIDTH//3):
    for y in range(0, HEIGHT, blck_width):
        for x in range(0, WIDTH, blck_height):
            # pygame.draw.rect(screen, BLUE, rect, 1)
            yield Button(pygame.Rect(x, y, blck_width, blck_height))


pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
SCREEN.fill(WHITE)
cross_img = pygame.transform.scale(pygame.image.load("cross.png"), (BUTTON_WIDTH, BUTTON_HEIGHT))
circle_img = pygame.transform.scale(pygame.image.load("circle.png"), (BUTTON_WIDTH, BUTTON_HEIGHT))

buttons = np.array(list(grid())).reshape((3, 3))
gen = iter(buttons.flatten())
# quit_button = pygame.Rect(2, 2, 50, 50)
# pygame.draw.rect(SCREEN, BLUE, quit_button)

player = PLAYER_1
player_mapping = {PLAYER_1: cross_img, PLAYER_2: circle_img}
running = True

while running:
    event = pygame.event.poll()
    if event.type == MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        print("Clicked!")
        r, c = clicked_on_who(mouse_x, mouse_y, buttons)
        if not buttons[r][c].is_clickable():
            continue
        game_grid[r][c] = player
        buttons[r][c].add_image(player_mapping[player], SCREEN)
        buttons[r][c].clickable = False
        #if finished(r, c, player):
        #    print(f"Player {player} wins!")
        #    break
        player = PLAYER_2 if player == PLAYER_1 else PLAYER_1

    try:
        # Draw the next rectangle from the generator
        b = next(gen)
        pygame.draw.rect(SCREEN, BLUE, b, 1)
    except StopIteration:
        # If the generator is exhausted, recreate it
        gen = iter(buttons.flatten())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ITERS+=1
    pygame.display.update()

pygame.quit()