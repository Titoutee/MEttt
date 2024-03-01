import numpy as np
from time import sleep
import pygame
import os
import pygame_menu
from GUIext import *
from random import randint

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

one_player = False
difficult = False

def start():
    global one_player, difficult
    one_player = player_selector.get_value()[0][1]
    difficult = difficult_selector.get_value()[0][1]
    menu.disable()

def grid_full():
    return ITERS >= 9

def nones_f():
    return [(r, c) for r, row in enumerate(game_grid) for c, val in enumerate(row) if val == None]

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
        return True
    if game_grid[0][2] != None and game_grid[0][2] == game_grid[1][1] == game_grid[2][0]:
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

WIN = 4 #Superior score

def best_fit(r, c):
    max_count_from_1 = count_from(r, c, PLAYER_1)
    max_count_from_2 = count_from(r, c, PLAYER_2)
    if max_count_from_2 >= 3:
        return WIN
    return max(max_count_from_1, max_count_from_2)

def move():
    l = sorted(nones_f(), key=lambda pos: best_fit(*pos))
    print(l)
    return l[-1]

def grid(blck_height = BUTTON_HEIGHT, blck_width = BUTTON_WIDTH):
    for y in range(0, HEIGHT, blck_width):
        for x in range(0, WIDTH, blck_height):
            # pygame.draw.rect(screen, BLUE, rect, 1)
            yield Button(pygame.Rect(x, y, blck_width, blck_height))

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

basic_font = pygame.font.Font(None, 64)
menu = pygame_menu.Menu(title="Morpion", width=WIDTH, height=HEIGHT, theme=pygame_menu.themes.THEME_DARK)
player_selector = menu.add.selector(title="Nombre joueurs: ", items=[("1", True), ("2", False)])
difficult_selector = menu.add.selector(title="Difficulté: ", items=[("Facile", False), ("Difficile", True)])
menu.add.button('Start', start)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(SCREEN)

exe_dir = os.path.dirname(os.path.abspath(__file__))
cross_img = pygame.transform.scale(pygame.image.load(os.path.join(exe_dir, "images", "cross.png")), (BUTTON_WIDTH, BUTTON_HEIGHT))
circle_img = pygame.transform.scale(pygame.image.load(os.path.join(exe_dir, "images", "circle.png")), (BUTTON_WIDTH, BUTTON_HEIGHT))


while 1:
    # Reinit game at each iteration
    game_grid = [[None]*3 for _ in range(3)]
    ITERS = 0
    player = PLAYER_1
    player_mapping = {PLAYER_1: cross_img, PLAYER_2: circle_img}
    running = True
    r = c = 0
    vol_quit = False
    buttons = np.array(list(grid())).reshape((3, 3))
    gen = iter(buttons.flatten()) # will be constantly emptied and refilled for grid displaying

    SCREEN.fill(WHITE) # Dump the menu UI
    while running:
        try:
            pygame.draw.rect(SCREEN, BLUE, next(gen), 1)
        except StopIteration:
            gen = iter(buttons.flatten())
        pygame.display.update()
    
        if player == PLAYER_2 and one_player:
            nones = nones_f()
            r, c = move() if difficult else nones[randint(0, len(nones)-1)]
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
            print(f"Le joueur {player} gagne!")
            wtext = "L'ordinateur a gagné !" if one_player and player == PLAYER_2 else "Le joueur 1 a gagné !"
            win_text = basic_font.render(wtext, True, (0, 0, 0), (255, 255, 255))
            win_text_surf = win_text.get_rect()
            win_text_surf.center = (WIDTH // 2, HEIGHT // 4)
            bg_rect = pygame.Rect(0,0,win_text_surf[2]+3, win_text_surf[3]+3)
            bg_rect.center = (WIDTH//2, HEIGHT//4)
            background = pygame.draw.rect(SCREEN, (0, 0, 0), bg_rect, width = 5)
            SCREEN.blit(win_text, win_text_surf)
            
            retry = basic_font.render("Rejouer", True, (0, 0, 0), (255, 255, 255))
            retry_surf = retry.get_rect()
            retry_surf.center = (WIDTH // 2, HEIGHT // 2)
            bg_rect = pygame.Rect(0,0,retry_surf[2]+3, retry_surf[3]+3)
            bg_rect.center = (WIDTH//2, HEIGHT//2)
            background = pygame.draw.rect(SCREEN, (0, 0, 0), bg_rect, width = 5)
            SCREEN.blit(retry, retry_surf)
            for events in pygame.event.get():
                if events.type == pygame.MOUSEBUTTONDOWN and bg_rect.collidepoint(events.pos):
                    start()
            


            back = basic_font.render("Retour", True, (0, 0, 0), (255, 255, 255))
            back_surf = back.get_rect()
            back_surf.center = (WIDTH // 2, 3*HEIGHT // 4)
            bg_rect = pygame.Rect(0,0,back_surf[2]+3, back_surf[3]+3)
            bg_rect.center = (WIDTH//2, 3*HEIGHT//4)
            background = pygame.draw.rect(SCREEN, (0, 0, 0), bg_rect, width = 5)
            SCREEN.blit(back, back_surf)
            break

        if grid_full():
            print(f"La grille est pleine! Match nul.")
            draw_text = basic_font.render("La grille est pleine ! Match nul", True, (0, 0, 0), (255, 255, 255))
            draw_text_surf = draw_text.get_rect()
            draw_text_surf.center = (WIDTH // 2, HEIGHT // 4)
            bg_rect = pygame.Rect(0,0,draw_text_surf[2]+3, draw_text_surf[3]+3)
            bg_rect.center = (WIDTH//2, HEIGHT//4)
            background = pygame.draw.rect(SCREEN, (0, 0, 0), bg_rect, width = 5)
            SCREEN.blit(draw_text, draw_text_surf)
            break
        
        player = PLAYER_2 if player == PLAYER_1 else PLAYER_1
    
    if not vol_quit:
        while not pygame.event.peek(eventtype=MOUSEBUTTONDOWN):
            pygame.display.update()
    menu.enable()
    menu.mainloop(SCREEN)
