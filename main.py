import numpy as np
import pygame

RATIO = (1, 1)
HEIGHT = 720
WIDTH = HEIGHT//RATIO[0]*RATIO[1]
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

PLAYER_1 = 1
PLAYER_2 = 2
player = PLAYER_1
grid = [[None]*3 for i in range(3)]
winners = {PLAYER_1: [], PLAYER_2: []}

def grid_full():
    return all(x!=None for line in grid for x in line)

def game_round(r, c):
    global player
    grid[r][c] = player
    player = PLAYER_2 if player == PLAYER_1 else PLAYER_1
    print_grid()

def print_grid():
    for i in range(len(grid)):
        # print("_ _ _")
        for j in range(len(grid[0])):
            print(f"|{player_mapping[grid[i][j]]}", end="")
        print("|")

def finished(r, c, player):
    if grid.count(player) == 3:
        return True
    for line in grid:
        if line[0] != player:
            break
    else:
        return True
    if grid[0][0] == grid[1][1] == grid[2][2]:
        return True
    return False

def grid(blck_height = HEIGHT//3, blck_width = WIDTH//3):
    for x in range(0, WIDTH, blck_height):
        for y in range(0, HEIGHT, blck_width):
            # pygame.draw.rect(screen, BLUE, rect, 1)
            yield pygame.Rect(x, y, blck_width, blck_height)

# cross_img = pygame.image.load("cross.png")
# circle_img = pygame.image.load("circle.png")

player_mapping = {PLAYER_1: "X", PLAYER_2: "O", None: " "}

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
SCREEN.fill(WHITE)
buttons = grid()

# quit_button = pygame.Rect(2, 2, 50, 50)
# pygame.draw.rect(SCREEN, BLUE, quit_button)

running = True
while running:
    #while not grid_full():
    #    event = None
    #    while event != pygame.MOUSEBUTTONDOWN:
    #        event = pygame.event.wait()
    #    mouse_x, mouse_y = pygame.mouse.get_pos()
    #    if quit_button.collidepoint(mouse_x, mouse_y):
    #        print("Hey")

    #    # print(r, c)
    #    # grid[r][c] = player

    #    # print_grid()
    #    # if finished(r, c, player):
    #    #     print(f"Player {player} wins!")
    #    #     break
    #    # player = PLAYER_2 if player == PLAYER_1 else PLAYER_1
    #else:
    #    print("Full game!")
    #print("Finished!")
    try:
        # Draw the next rectangle from the generator
        b = next(buttons)
        pygame.draw.rect(SCREEN, BLUE, b, 1)
    except StopIteration:
        # If the generator is exhausted, recreate it
        buttons = grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()