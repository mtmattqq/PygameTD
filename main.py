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
import numpy as np
import math
import random

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
MOVEMENT = [[1, 0], [0, 1], [-1, 0], [0, -1]]

def show_text(text = '', x = 0, y = 0, color = (0, 0, 0), size = 0) :
    font=pygame.font.SysFont('unifont', size)
    text=font.render(text, True, color)
    textRect=text.get_rect()
    textRect.topleft=(x-10, y-20)
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

def select_tile(mouse_pos, tower_info, towers, map_info) :
    tile_pos = [mouse_pos.y // 64, mouse_pos.x // 64]
    selected_tile = 0
    show_buy_tower = False
    show_tower_info = False

    if(
        tile_pos[0] < 9 and 
        tile_pos[1] < 12 and 
        map_info[tile_pos[0]][tile_pos[1]] != 1 and
        map_info[tile_pos[0]][tile_pos[1]] != 2 and
        map_info[tile_pos[0]][tile_pos[1]] != 3
    ) :
        selected_tile = tile_pos
        if tower_info[tile_pos[0], tile_pos[1]] == 0 :
            show_buy_tower = True
            show_tower_info = False
        else :
            show_buy_tower = False
            show_tower_info = True
    selected_tower = None
    for tow in towers :
        if tow.detect_mouse(mouse_pos) :
            selected_tower = tow
    return (selected_tile, show_buy_tower, show_tower_info, selected_tower)

def level() :
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

    level_map = tile.tilemap(tile_set, level_info['map_size'])
    level_map.set_zero()
    level_map.load(level_info['map'])
    level_map.render()
    level_path = find_path(level_info['map'])
    
    # for pos in level_path :
    #     print(pos.get_tuple())


    towers = []
    tower_info = np.zeros(level_info['map_size'], dtype=int)
    show_tower_info = False
    selected_tower = None

    ENEMY_TYPE = 2
    enemys = []
    enemy_types = [
        enemy.basic_enemy(level_path[0].copy(), 0, 0, 0, 20, level_path),
        enemy.evil_eye(level_path[0].copy(), 0, 0, 0, 25, level_path)
    ]
    enemy_level = [
        0, 0
    ]
    enemy_base_info = [
        [[30, 0, 0, 20], [1, 0, 0, 0]], 
        [[10, 5, 20, 25], [0.5, 0, 0.1, 0]]
    ]
    enemy_type_this_wave = 0
    enemy_type_next_wave = 0

    time_previous = 0
    game_timer = 0

    wave = level_info['start_wave']
    for i in range(ENEMY_TYPE) :
        enemy_level[i] = math.ceil(wave / ENEMY_TYPE)
    wave_interval = 5000
    send_next_wave = 10000
    send_this_wave = 0
    sending_wave = False
    send_next_enemy = 0
    enemy_dencity = 1000
    sent_enemy = 0

    # money
    natural_ingot = level_info['start_money']
    natural_ingot_button = button(
        'Natural Ingot', vec2D(785, 16), 
        [0, 0, 0], 32, 32, ['natural_ingot16.png']
    )

    # row col -> y, x
    selected_tile = [0, 0]

    tile_rect = pygame.Rect([0, 0], [tile.TILE_SIZE, tile.TILE_SIZE])

    # buy tower button
    show_buy_tower = False
    def buy_tower_buttons_onclick() :
        return True
    buy_tower_buttons = [
        button(
            80, vec2D(785, 48), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'basic_tower32.png'], 
            buy_tower_buttons_onclick
        ),

        button(
            150, vec2D(845, 48), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'sniper_tower32.png'], 
            buy_tower_buttons_onclick
        ),

        button(
            300, vec2D(905, 48), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'cannon_tower32.png'], 
            buy_tower_buttons_onclick
        )
    ]

    # sent next wave
    sent_next_wave_button = button(
        'sent_next_wave', vec2D(775, 490), 
        [0, 0, 0], 32, 32, 
        ['start_button.png'], 
        buy_tower_buttons_onclick
    )

    in_game = True
    while in_game :
        time_now = pygame.time.get_ticks()
        delta_time = time_now - time_previous
        time_previous = time_now
        game_timer += delta_time

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2D(mouse_pos[0],mouse_pos[1])

        if game_timer > send_next_wave :
            wave += 1
            enemy_level[enemy_type_this_wave] += 1
            send_this_wave = send_next_wave
            enemy_type_this_wave = enemy_type_next_wave
            enemy_type_next_wave = random.randint(0, ENEMY_TYPE - 1)
            enemy_dencity = max(300, 1000-10*enemy_level[enemy_type_this_wave])
            wave_interval = math.ceil(math.sqrt(enemy_level[enemy_type_this_wave]) * enemy_dencity) + 5000
            send_next_wave += wave_interval
            sending_wave = True
            sent_enemy += math.floor(math.sqrt(enemy_level[enemy_type_this_wave])) + 1
            send_next_enemy = 0
            

        if sending_wave and game_timer >= send_next_enemy+send_this_wave :
            send_next_enemy += enemy_dencity
            nen = enemy_types[enemy_type_this_wave].copy()
            nen.__init__(
                level_path[0].copy(), 
                enemy_base_info[enemy_type_this_wave][0][0] + enemy_base_info[enemy_type_this_wave][1][0] * (enemy_level[enemy_type_this_wave]**2), 
                enemy_base_info[enemy_type_this_wave][0][1] + enemy_base_info[enemy_type_this_wave][1][1] * (enemy_level[enemy_type_this_wave]**2), 
                enemy_base_info[enemy_type_this_wave][0][2] + enemy_base_info[enemy_type_this_wave][1][2] * (enemy_level[enemy_type_this_wave]**2),
                enemy_base_info[enemy_type_this_wave][0][3], level_path
            )
            enemys.append(nen)
            sent_enemy -= 1
            if sent_enemy == 0 :
                sending_wave = False

        for tow in towers :
            tow.update(delta_time, enemys)
        for en in enemys :
            if not en.alive :
                enemys.remove(en)
                natural_ingot += en.max_hit/10
            en.update(delta_time)

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                in_game = False
            if event.type == pygame.KEYDOWN :
                if event.unicode == 'q' :
                    in_game = False
                if event.unicode == 'u' :
                    if selected_tower != None :
                        for i in range(100000) :
                            clicked_upgrade, natural_ingot = selected_tower.upgrade(
                                mouse_pos, natural_ingot
                            )
                            if clicked_upgrade :
                                continue
                if sent_next_wave_button.click(mouse_pos) :
                    for i in range(10000) :
                        wave += 1
                        enemy_level[enemy_type_this_wave] += 1
                        send_this_wave = send_next_wave
                        enemy_type_this_wave = enemy_type_next_wave
                        enemy_type_next_wave = random.randint(0, ENEMY_TYPE - 1)
                        enemy_dencity = max(300, 1000-10*enemy_level[enemy_type_this_wave])
                        wave_interval = math.ceil(math.sqrt(enemy_level[enemy_type_this_wave]) * enemy_dencity) + 3000 
                        send_next_wave += wave_interval
                        sending_wave = True
                        sent_enemy += math.floor(enemy_level[enemy_type_this_wave]) + 1
                        send_next_enemy = 0
                    game_timer = send_next_wave
                        
            if event.type == pygame.MOUSEBUTTONDOWN : 
                mouse = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP and mouse[0] :
                mouse = [False, False, False]
                ct = 1
                for buy_tower in buy_tower_buttons :
                    if(
                        show_buy_tower and 
                        buy_tower.click(mouse_pos) and 
                        buy_tower.text <= natural_ingot
                    ) :
                        natural_ingot -= buy_tower.text
                        tower_info[selected_tile[0], selected_tile[1]] = ct
                        new_tower = None
                        if ct == 1 :
                            new_tower = tower.basic_tower(vec2D(selected_tile[1], selected_tile[0]))
                        elif ct == 2 :
                            new_tower = tower.sniper_tower(vec2D(selected_tile[1], selected_tile[0]))
                        elif ct == 3 :
                            new_tower = tower.cannon_tower(vec2D(selected_tile[1], selected_tile[0]))
                        new_tower.place(vec2D(selected_tile[1], selected_tile[0]))
                        towers.append(new_tower)
                    ct += 1 
                
                if selected_tower != None :
                    clicked_upgrade, natural_ingot = selected_tower.upgrade(
                        mouse_pos, natural_ingot
                    )
                    if clicked_upgrade :
                        continue

                if sent_next_wave_button.click(mouse_pos) :
                    send_next_wave = game_timer
                selected_tile, show_buy_tower, show_tower_info, selected_tower = select_tile(
                    mouse_pos, tower_info, towers, level_info['map']
                )


        # display
        screen.fill((245, 245, 245))
        screen.blit(level_map.image, level_map.rect)

        if show_buy_tower or show_tower_info :
            tile_rect.center = transform(
                vec2D(selected_tile[1], selected_tile[0]), 
                tile.TILE_SIZE
            ).get_tuple()
            color = pygame.Color(100, 120, 180, a=2)
            pygame.draw.rect(
                screen, color, 
                tile_rect, 0
            )
        
        for tow in towers :
            tow.display(screen)
        for tow in towers :
            tow.display_bullets(screen)
        for en in enemys :
            en.display(screen)
        sent_next_wave_button.display(screen)
        show_text(
            'Next wave in {:.2f} s.'.format((send_next_wave - game_timer)/1000), 
            790, 545, (0, 0, 0), 20
        )
        show_text(
            'Wave : {}'.format(wave), 
            790, 570, (0, 0, 0), 20
        )
        
        natural_ingot_button.display(screen)
        show_text(str(natural_ingot), 850, 40, (0, 0, 0), 20)
        if show_buy_tower :
            for buy_tower in buy_tower_buttons :
                if buy_tower.text > natural_ingot :
                    buy_tower.state = 1
                    buy_tower.display(screen)
                else :
                    buy_tower.state = 0
                    buy_tower.display(screen)
                buy_tower.state = 2
                buy_tower.display(screen)
            
        elif show_tower_info :
            color = pygame.Color(30, 30, 30, a=70)
            pygame.draw.circle(
                screen, color, 
                selected_tower.location.get_tuple(), 
                selected_tower.range,
                3
            )

            selected_tower.display_info(screen, natural_ingot)
        
        if not show_tower_info :
            selected_tower = None
        
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
        mouse_pos = vec2D(mouse_pos[0], mouse_pos[1])

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                in_game = False
            if event.type == pygame.KEYDOWN :
                if event.unicode == 'q' :
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                start_button.detect(pos = mouse_pos)
            if event.type == pygame.MOUSEBUTTONUP :
                if start_button.click(mouse_pos) :
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