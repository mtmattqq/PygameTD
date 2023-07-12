import pygame
import copy
from pygame.locals import *
from vec2D import vec2D
from vec2D import transform
from button import button
import tile
import json
import os
import tower
import enemy

# pygame init
pygame.init()
flags = DOUBLEBUF | SCALED | FULLSCREEN
resolution = (1024, 576)
screen = pygame.display.set_mode(resolution, flags, 16)
screen.fill((245, 245, 245))
clock = pygame.time.Clock()
pygame.display.set_caption("Basic TD Game")
font = 'unifont'
pygame.event.set_allowed([
    QUIT, KEYDOWN, KEYUP, 
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, 
    MOUSEMOTION, MOUSEWHEEL])

# variables
FPS=60
relative_pos = vec2D(0, 0)
MOVEMENT = [[1, 0], [0, 1], [-1, 0], [0, -1]]

def show_text(text = '', x = 0, y = 0, color = (0, 0, 0), size = 0) :
    font=pygame.font.SysFont('unifont', size)
    text=font.render(text, True, color)
    textRect=text.get_rect()
    textRect.topleft=(x+relative_pos.x-10, y+relative_pos.y-20)
    screen.blit(text, textRect)

def find_path(map = [[]]) :
    m = len(map)
    n = len(map[0])
    enemy_source = []
    main_tower = []
    for i in range(m) :
        for j in range(n) :
            if map[i][j] == 1 :
                main_tower = [i, j]
            elif map[i][j] == 2 :
                enemy_source = [i, j]
    isv = []
    for i in range(m) :
        line = []
        for j in range(n) :
            line.append(False)
        isv.append(line)

    path = []
    pos_now = enemy_source
    ct = 0
    while pos_now != main_tower :
        ct += 1 
        if ct > 1000 :
            return path
        isv[pos_now[0]][pos_now[1]] = True
        path.append(transform(vec2D(pos_now[1], pos_now[0]), tile.TILE_SIZE))
        for d in MOVEMENT :
            next_stap = [pos_now[0] + d[0], pos_now[1] + d[1]]
            if(
                next_stap[0] >= 0 and next_stap[1] >= 0 and
                next_stap[0] < m and next_stap[1] < n and
                (map[next_stap[0]][next_stap[1]] == 3 or
                 map[next_stap[0]][next_stap[1]] == 1) and 
                not isv[next_stap[0]][next_stap[1]]
            ) :
                pos_now = next_stap
                break
    return path

def level() :
    global enemy
    tile_set = tile.tileset([
        'white.png',
        'main_tower.png',
        'enemy_sourse.png',
        'road.png'
    ], 64, 64)
    level_info_file = open(os.path.join(os.getcwd(), 'AppData', 'basic_level.json'), 'r')
    level_info = level_info_file.read()
    # print(level_info)
    level_info = json.loads(level_info)
    level_info_file.close()

    # print(level_info['map_size'])

    level_map = tile.tilemap(tile_set, level_info['map_size'])
    level_map.set_zero()
    level_map.load(level_info['map'])
    level_map.render()
    level_path = find_path(level_info['map'])
    
    # for pos in level_path :
    #     print(pos.get_tuple())

    # testing 
    t1 = tower.basic_tower(vec2D(4, 5))
    e1 = enemy.basic_enemy(level_path[0], 100, 0, 0, 20, level_path)

    enemys = [e1]

    time_previous = 0
    game_timer = 0
    in_game = True
    while in_game :
        time_now = pygame.time.get_ticks()
        delta_time = time_now - time_previous
        time_previous = time_now
        game_timer += delta_time

        t1.shoot(enemys)
        t1.update(delta_time, enemys)
        for en in enemys :
            if en.hit <= 0 :
                enemys.remove(en)
            en.move(delta_time)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2D(mouse_pos[0],mouse_pos[1])

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                in_game = False
            if event.type == pygame.KEYDOWN :
                if event.unicode == 'q' :
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                a=0
            if event.type == pygame.MOUSEBUTTONUP :
                a=0
        
        

        # display
        screen.fill((245, 245, 245))
        screen.blit(level_map.image, level_map.rect)
        t1.display(screen)
        for en in enemys :
            en.display(screen)
        # rect = tile_set.tiles[1].get_rect()
        # rect.topleft = (100, 100)
        # screen.blit(tile_set.tiles[1], rect)
        pygame.display.update()
        clock.tick(FPS)
    return

def main_page() :
    def click_start_button() :
        return True
    start_button = button('Start', vec2D(resolution[0]/2-64, resolution[1]/2-64), 
                          [0, 0, 0], 128, 128, 
                          ['start_button.png'], click_start_button)
    start_button.pos = vec2D(
        resolution[0]/2-start_button.width/2, 
        resolution[1]/2-start_button.height/2+50)
    title = 'Basic TD'

    in_game=True
    while in_game :
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2D(mouse_pos[0],mouse_pos[1])

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                in_game = False
            if event.type == pygame.KEYDOWN :
                if event.unicode == 'q' :
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                start_button.detect(pos = mouse_pos+relative_pos)
            if event.type == pygame.MOUSEBUTTONUP :
                if start_button.click(mouse_pos+relative_pos) :
                    level()
        
        # display
        screen.fill((245, 245, 245))
        start_button.display(screen)
        show_text(title, 300, 175, (0, 0, 0), 108)
        pygame.display.update()
        clock.tick(FPS)
    return

main_page()
pygame.quit()