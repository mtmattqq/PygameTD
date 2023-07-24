import pygame
from pygame.locals import *
import os
from button import button
from vec2D import vec2D
from vec2D import transform

# pygame init
pygame.init()
pygame.font.init()
pygame.mixer.init()
flags = DOUBLEBUF | SCALED | FULLSCREEN
resolution = (1024, 576)
screen = pygame.surface.Surface(resolution)
display = pygame.display.set_mode(resolution, flags, 32)
screen.fill((245, 245, 245))
clock = pygame.time.Clock()
pygame.display.set_caption("Basic TD Game")
font = 'unifont'
pygame.event.set_allowed([
    QUIT, KEYDOWN, KEYUP, 
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, 
    MOUSEMOTION, MOUSEWHEEL,
    FINGERDOWN, FINGERUP, FINGERMOTION
])
pygame.display.set_icon(pygame.image.load(os.path.join(os.getcwd(), 'AppData', 'icon.png')))

def show_text(text = '', x = 0, y = 0, color = (0, 0, 0), size = 0) :
    font=pygame.font.Font(os.path.join(os.getcwd(), 'AppData', 'unifont.ttf'), size)
    text=font.render(text, True, color)
    textRect=text.get_rect()
    textRect.topleft=(x-10, y-20)
    screen.blit(text, textRect)

# loading

loading_bar_red = button('', vec2D(resolution[0]/2-64, resolution[1]/2-64), 
                        [0, 0, 0], 256, 256, 
                        ['hit_bar_red.png'])
loading_bar_red.pos = vec2D(
    resolution[0] / 2 - loading_bar_red.width / 2, 
    resolution[1] / 2 - loading_bar_red.height / 2 + 50)
loading_bar_green = button('', vec2D(resolution[0]/2-64, resolution[1]/2-64), 
                        [0, 0, 0], 256, 256, 
                        ['hit_bar_green.png']
)
loading_bar_green.pos = vec2D(
    (resolution[0] / 2) - loading_bar_green.width / 2, 
    (resolution[1] / 2) - loading_bar_green.height / 2 + 50)    

title = 'Loading'
progress = 0

def display_things() :
    # display
    screen.fill((255, 255, 255))
    loading_bar_red.display(screen)
    loading_bar_green_image = pygame.transform.scale(
        loading_bar_green.images[0], 
        [loading_bar_green.width * (progress / 100), loading_bar_green.height]
    )
    show_text(title, 300, 175, (0, 0, 0), 108)
    screen.blit(loading_bar_green_image, loading_bar_green.pos.get_tuple())
    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.update()
display_things()

import tile
progress = 30
pygame.time.delay(300)
display_things()

import tower
import enemy
progress = 50
pygame.time.delay(300)
display_things()

import numpy as np
import math
import random
import json
progress = 80
pygame.time.delay(300)
display_things()

import copy
progress = 100
display_things()

pygame.time.delay(300)
# end loading

# variables
FPS=60
MOVEMENT = [[1, 0], [0, 1], [-1, 0], [0, -1]]
is_fullscreen = True
volume = 100



def game_over() :
    def click_start_button() :
        return True
    start_button = button('Start', vec2D(resolution[0]/2-64, resolution[1]/2-64), 
                          [0, 0, 0], 128, 128, 
                          ['start_button.png'], click_start_button)
    start_button.pos = vec2D(
        resolution[0]/2-start_button.width/2, 
        resolution[1]/2-start_button.height/2+50)
    title = 'Game Over'

    in_game=True
    while in_game :
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2D(mouse_pos[0], mouse_pos[1])

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.unicode == 'q' :
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                start_button.detect(pos = mouse_pos)
            if event.type == pygame.MOUSEBUTTONUP :
                if start_button.click(mouse_pos) :
                    in_game = False
        
        # display
        screen.fill((200, 200, 200))
        start_button.display(screen)
        show_text(title, 300, 175, (0, 0, 0), 98)
        display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    return

def setting() :
    global flags, screen, display, is_fullscreen, volume
    fullscreen_button = button(
        'fullscreen', vec2D(resolution[0] / 2 - 128 + 100, resolution[1] / 2 - 16 - 50), 
        [0, 0, 0], 256, 32, 
        ['select_level.png']
    )
    set_volume_button = button(
        'fullscreen', vec2D(resolution[0] / 2 - 16 - 100, resolution[1] / 2 - 16 + 50), 
        [0, 0, 0], 32, 32, 
        ['set_volume.png']
    )
    
    input_file = open(os.path.join(os.getcwd(), 'AppData', 'setting.json'), 'r')
    input = input_file.read()
    input = json.loads(input)
    input_file.close()

    is_fullscreen = input['is_fullscreen']
    volume = input['volume']
    is_set_volume_bar_pressed = False
    
    title = 'Setting'

    in_game=True
    while in_game :
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2D(mouse_pos[0], mouse_pos[1])

        if is_set_volume_bar_pressed :
            mouse_pos.x
            volume = (mouse_pos.x - (resolution[0] / 2 - 16 - 20)) / 256 * 100 - 7
            volume = max(0, min(100, volume))

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE : 
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN : 
                if set_volume_button.click(mouse_pos) :
                    is_set_volume_bar_pressed = True
            if event.type == pygame.MOUSEBUTTONUP :
                if fullscreen_button.click(mouse_pos) :
                    if is_fullscreen :
                        is_fullscreen = False
                        flags = DOUBLEBUF
                    else :
                        is_fullscreen = True
                        flags = DOUBLEBUF | SCALED | FULLSCREEN
                    display = pygame.display.set_mode(resolution, flags, 32)
                is_set_volume_bar_pressed = False
        
        # display
        screen.fill((245, 245, 245))
        show_text(title, 330, 70, [0, 0, 0], 108)
        fullscreen_button.display(screen)
        show_text('Fullscreen : ', 275, 237, [0, 0, 0], 36)
        show_text(str(is_fullscreen), 580, 237, [0, 0, 0], 36)

        show_text('Volume : ', 335, 337, [0, 0, 0], 36)
        show_text('{:.0f}'.format(volume), 780, 337, [0, 0, 0], 36)
        set_volume_button.pos.x = resolution[0] / 2 - 16 - 20 + (volume * 256 / 100)
        pygame.draw.line(
            screen, [0, 0, 0], 
            [resolution[0] / 2 - 16, resolution[1] / 2 - 16 + 65], 
            [resolution[0] / 2 - 16 + 250, resolution[1] / 2 - 16 + 65], 2
        )
        set_volume_button.display(screen)
        

        display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    
    input['is_fullscreen'] = is_fullscreen
    input['volume'] = volume
    output = open(os.path.join(os.getcwd(), 'AppData', 'setting.json'), 'w')
    output.write(json.dumps(input))
    return

def find_path(map = [[]]) :
    m = len(map)
    n = len(map[0])
    def in_boarder(r, c) :
        return (
            r >= 0 and c >= 0 and
            r < m and c < n
        )
    enemy_source = None
    main_tower = None
    for i in range(m) :
        for j in range(n) :
            if map[i][j] == 1 :
                main_tower = [i, j]
            elif map[i][j] == 2 :
                enemy_source = [i, j]
    if enemy_source == None or main_tower == None :
        return None
    isv = []
    for i in range(m) :
        line = []
        for j in range(n) :
            line.append(False)
        isv.append(line)

    path = []
    pos_now = enemy_source
    ct = 0

    def dfs(pos_now = []) :
        isv[pos_now[0]][pos_now[1]] = True
        for d in MOVEMENT :
            next_stap = [pos_now[0] + d[0], pos_now[1] + d[1]]
            if(
                in_boarder(next_stap[0], next_stap[1]) and
                (map[next_stap[0]][next_stap[1]] == 3 or
                 map[next_stap[0]][next_stap[1]] == 1) and 
                not isv[next_stap[0]][next_stap[1]]
            ) :
                path.append(transform(vec2D(pos_now[1], pos_now[0]), tile.TILE_SIZE))
                if map[next_stap[0]][next_stap[1]] == 1 or dfs(next_stap) :
                    return True
                path.pop()
                break
        return False
    if dfs(enemy_source) :
        path.append(transform(vec2D(main_tower[1], main_tower[0]), tile.TILE_SIZE))
        return path
    else :
        return None
    # while pos_now != main_tower :
    #     ct += 1 
    #     if ct > 1000 :
    #         return path
    #     isv[pos_now[0]][pos_now[1]] = True
    #     path.append(transform(vec2D(pos_now[1], pos_now[0]), tile.TILE_SIZE))
    #     for d in MOVEMENT :
    #         next_stap = [pos_now[0] + d[0], pos_now[1] + d[1]]
    #         if(
    #             next_stap[0] >= 0 and next_stap[1] >= 0 and
    #             next_stap[0] < m and next_stap[1] < n and
    #             (map[next_stap[0]][next_stap[1]] == 3 or
    #              map[next_stap[0]][next_stap[1]] == 1) and 
    #             not isv[next_stap[0]][next_stap[1]]
    #         ) :
    #             pos_now = next_stap
    #             break
    # path.append(transform(vec2D(main_tower[1], main_tower[0]), tile.TILE_SIZE))
    # return path

def select_tile(
    mouse_pos, 
    tower_info, 
    towers, 
    map_info, 
    show_tower_info, 
    selected_tile, 
    selected_tower
) :
    tile_pos = [mouse_pos.y // 64, mouse_pos.x // 64]
    show_buy_tower = False

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

    for tow in towers :
        if tow.detect_mouse(mouse_pos) :
            selected_tower = tow
    return (selected_tile, show_buy_tower, show_tower_info, selected_tower)

def level(level_now = 'basic_level.json') :
    tile_set = tile.tileset([
        'white.png',
        'main_tower.png',
        'enemy_sourse.png',
        'road.png'
    ], 64, 64)
    level_info_file = open(os.path.join(os.getcwd(), 'AppData', level_now), 'r')
    level_info = level_info_file.read()
    # print(level_info)
    level_info = json.loads(level_info)
    level_info_file.close()

    level_map = tile.tilemap(tile_set, level_info['map_size'])
    level_map.set_zero()
    level_map.load(level_info['map'])
    level_map.render()
    level_path = find_path(level_info['map'])


    towers = []
    tower_info = np.zeros(level_info['map_size'], dtype=int)
    show_tower_info = False
    selected_tower = None

    ENEMY_TYPE = 3
    enemys = []
    
    enemy_types = [
        enemy.basic_enemy(vec2D(800, 140), 0, 0, 0, 0, level_path),
        enemy.evil_eye(vec2D(800, 220), 0, 0, 0, 0, level_path), 
        enemy.high_armor(vec2D(800, 300), 0, 0, 0, 0, level_path)
    ]
    for en in enemy_types :
        en.location = en.pos
    enemy_level = [
        0, 0, 5
    ]
    enemy_base_info = [
        [[30,  0,  0,  30, 300], [1.5,    0,    0,   1, 30]], 
        [[10,  5, 20,  40, 300], [0.1, 0.05,  1.4,   1, 30]], 
        [[30, 10,  1,  25, 300], [  5,    1, 0.05, 0.1, 30]],
    ]
    
    boss_types = [
        enemy.basic_boss(vec2D(785, 80), 0, 0, 0, 10, [vec2D(785, 80)]), 
        enemy.eye_boss(vec2D(785, 140), 0, 0, 0, 10, [vec2D(785, 140)]), 
        enemy.high_armor_boss(vec2D(785, 200), 0, 0, 0, 10, [vec2D(785, 200)])
    ]
    boss = None
    boss_level = 0

    enemy_type_this_wave = 0
    enemy_type_next_wave = 0

    time_previous = pygame.time.get_ticks()
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

    # bonus
    give_bonus_rate = 0.05
    give_bonus_wait_time = 10000
    give_bonus_time = give_bonus_wait_time
    give_bonus_bar = button(
        'Give_Bonus_Bar', vec2D(945, 6), 
        [0, 0, 0], 48, 48, ['hit_bar_red.png', 'hit_bar_blue.png']
    )

    # player health
    hit = level_info['start_hit']
    hit_button = button(
        'Player Health', vec2D(785, 48), 
        [0, 0, 0], 32, 32, ['main_tower.png']
    )

    # row col -> y, x
    selected_tile = [0, 0]

    tile_rect = pygame.Rect([0, 0], [tile.TILE_SIZE, tile.TILE_SIZE])

    difficulty = level_info['difficulty']

    # buy tower button
    show_buy_tower = False
    def buy_tower_buttons_onclick() :
        return True
    buy_tower_buttons = [
        button(
            80, vec2D(785, 80), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'basic_tower32.png'], 
            buy_tower_buttons_onclick
        ),

        button(
            150, vec2D(845, 80), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'sniper_tower32.png'], 
            buy_tower_buttons_onclick
        ),

        button(
            300, vec2D(905, 80), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'cannon_tower32.png'], 
            buy_tower_buttons_onclick
        ),

        button(
            400, vec2D(785, 140), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'tesla_tower32.png'], 
            buy_tower_buttons_onclick
        ),
    ]

    # sent next wave
    sent_next_wave_button = button(
        'sent_next_wave', vec2D(775, 490), 
        [0, 0, 0], 32, 32, 
        ['start_button.png'], 
        buy_tower_buttons_onclick
    )

    setting_button = button(
        'setting', vec2D(835, 490), 
        [0, 0, 0], 32, 32, 
        ['setting_button.png']
    )

    is_game_over = False
    is_sending_boss = False

    if wave >= 100 :
        # make basic enemy much stronger
        enemy_base_info[0][1][0] = 15
        enemy_base_info[0][1][3] = 3
        enemy_base_info[0][0][3] = 60
        enemy_base_info[0][0][4] = 150
        enemy_types[0] = enemy.angry_basic(enemy_types[0].pos, 0, 0, 0, 10, [enemy_types[0].pos])
        enemy_types[0].location = enemy_types[0].pos
    elif wave >= 125 :
        enemy_base_info[1][1][0] = 2.5
        enemy_base_info[1][1][1] = 1.25
        enemy_base_info[1][1][2] = 35
        enemy_base_info[1][1][3] = 15
        enemy_base_info[1][0][3] = 80
        enemy_base_info[1][0][4] = 135
        enemy_types[1] = enemy.chaos_eye(enemy_types[1].location, 0, 0, 0, 10, [enemy_types[1].pos])
        enemy_types[1].location = enemy_types[1].pos
    elif wave >= 150 :
        enemy_base_info[2][1][0] = 100
        enemy_base_info[2][1][1] = 40
        enemy_base_info[2][1][2] = 3
        enemy_base_info[2][1][3] = 1.5
        enemy_base_info[2][0][3] = 50
        enemy_base_info[2][0][4] = 150
        enemy_types[2] = enemy.super_shield(enemy_types[2].pos, 0, 0, 0, 10, [enemy_types[2].pos])
        enemy_types[2].location = enemy_types[2].pos
    
    
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
            # Enhance Enemy
            if wave >= 100 :
                # make basic enemy much stronger
                enemy_base_info[0][1][0] = 15
                enemy_base_info[0][1][3] = 3
                enemy_base_info[0][0][3] = 60
                enemy_base_info[0][0][4] = 150
                enemy_types[0] = enemy.angry_basic(enemy_types[0].pos, 0, 0, 0, 10, [enemy_types[0].pos])
                enemy_types[0].location = enemy_types[0].pos
            elif wave >= 125 :
                enemy_base_info[1][1][0] = 2.5
                enemy_base_info[1][1][1] = 1.25
                enemy_base_info[1][1][2] = 35
                enemy_base_info[1][1][3] = 15
                enemy_base_info[1][0][3] = 80
                enemy_base_info[1][0][4] = 135
                enemy_types[1] = enemy.chaos_eye(enemy_types[1].location, 0, 0, 0, 10, [enemy_types[1].pos])
                enemy_types[1].location = enemy_types[1].pos
            elif wave >= 150 :
                enemy_base_info[2][1][0] = 100
                enemy_base_info[2][1][1] = 40
                enemy_base_info[2][1][2] = 3
                enemy_base_info[2][1][3] = 1.5
                enemy_base_info[2][0][3] = 50
                enemy_base_info[2][0][4] = 150
                enemy_types[2] = enemy.super_shield(enemy_types[2].pos, 0, 0, 0, 10, [enemy_types[2].pos])
                enemy_types[2].location = enemy_types[2].pos

            if (wave >= 100 and wave % 25 == 0) or is_sending_boss :
                if boss != None :
                    boss_level += 3
                    is_sending_boss = True
                else :
                    is_sending_boss = False
                    enemy_type_this_wave = boss_level % 3
                    boss_level += 1
                    boss = boss_types[enemy_type_this_wave].copy()
                    base_hit = enemy_base_info[enemy_type_this_wave][0][0] + enemy_base_info[enemy_type_this_wave][1][0] * (enemy_level[enemy_type_this_wave]**2)
                    base_armor = enemy_base_info[enemy_type_this_wave][0][1] + enemy_base_info[enemy_type_this_wave][1][1] * math.sqrt(enemy_level[enemy_type_this_wave])
                    base_shield = enemy_base_info[enemy_type_this_wave][0][2] + enemy_base_info[enemy_type_this_wave][1][2] * (enemy_level[enemy_type_this_wave]**2)
                    boss.__init__(
                        level_path[0].copy(), 
                        base_hit * (difficulty / 100) * 10 * (boss_level ** 2), 
                        base_armor * (difficulty / 100) * 10 * (boss_level ** 2),
                        base_shield * (difficulty / 100) * 10 * (boss_level ** 2),
                        boss.move_speed, level_path
                    )

            # Generate Enemy
            enemy_type_this_wave = enemy_type_next_wave
            enemy_level[enemy_type_this_wave] += 1
            send_this_wave = send_next_wave
            enemy_type_next_wave = random.randint(0, min(math.floor(wave / 5), ENEMY_TYPE - 1))
            enemy_amount = math.floor(
                math.sqrt(
                    enemy_level[enemy_type_this_wave] * 
                    enemy_base_info[enemy_type_this_wave][1][3]
                )
            ) + 1
            enemy_dencity = max(
                enemy_base_info[enemy_type_this_wave][0][4], 
                1000-enemy_base_info[enemy_type_this_wave][1][4]*enemy_level[enemy_type_this_wave]
            )
            wave_interval = math.ceil(enemy_amount * enemy_dencity) + 5000
            send_next_wave += wave_interval
            sending_wave = True
            sent_enemy += enemy_amount
            send_next_enemy = 0
            
        if sending_wave and game_timer >= send_next_enemy+send_this_wave :
            send_next_enemy += enemy_dencity
            nen = enemy_types[enemy_type_this_wave].copy()
            base_hit = enemy_base_info[enemy_type_this_wave][0][0] + enemy_base_info[enemy_type_this_wave][1][0] * (enemy_level[enemy_type_this_wave]**2)
            base_armor = enemy_base_info[enemy_type_this_wave][0][1] + enemy_base_info[enemy_type_this_wave][1][1] * math.sqrt(enemy_level[enemy_type_this_wave])
            base_shield = enemy_base_info[enemy_type_this_wave][0][2] + enemy_base_info[enemy_type_this_wave][1][2] * (enemy_level[enemy_type_this_wave]**2)
            nen.__init__(
                level_path[0].copy(), 
                base_hit * difficulty / 100, 
                base_armor * difficulty / 100,
                base_shield * difficulty / 100,
                enemy_base_info[enemy_type_this_wave][0][3], level_path
            )
            enemys.append(nen)
            sent_enemy -= 1
            if sent_enemy == 0 :
                sending_wave = False

        for tow in towers :
            tow.update(delta_time, enemys, boss)
        for en in enemys :
            if en.update(delta_time) :
                hit -= 1
                if hit <= 0 :
                    is_game_over = True
                    in_game = False
            if not en.alive :
                enemys.remove(en)
                natural_ingot += math.sqrt(en.max_hit + en.max_shield)
        if boss != None :
            if boss.update(delta_time) :
                hit -= 1
                boss.pos = boss.location = level_path[0]
                boss.progress = 0
                if hit <= 0 :
                    is_game_over = True
                    in_game = False
            for en in boss.generated_unit :
                if en.update(delta_time) :
                    hit -= 1
                    if hit <= 0 :
                        is_game_over = True
                        in_game = False
                if not en.alive :
                    boss.generated_unit.remove(en)
            if boss.dead :
                natural_ingot += math.sqrt(boss.max_hit + boss.max_shield)
                boss = None

        if give_bonus_time > 0 :
            give_bonus_time -= delta_time
        else :
            give_bonus_time += give_bonus_wait_time
            natural_ingot += natural_ingot * give_bonus_rate

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    in_game = False
                        
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
                            new_tower = tower.basic_tower(vec2D(selected_tile[1], selected_tile[0]), volume)
                        elif ct == 2 :
                            new_tower = tower.sniper_tower(vec2D(selected_tile[1], selected_tile[0]))
                        elif ct == 3 :
                            new_tower = tower.cannon_tower(vec2D(selected_tile[1], selected_tile[0]))
                        elif ct == 4 :
                            new_tower = tower.tesla_tower(vec2D(selected_tile[1], selected_tile[0]))
                        new_tower.place(vec2D(selected_tile[1], selected_tile[0]))
                        towers.append(new_tower)
                    ct += 1 
                
                if selected_tower != None :
                    clicked_upgrade, natural_ingot = selected_tower.upgrade(
                        mouse_pos, natural_ingot
                    )
                    if clicked_upgrade :
                        continue
                    if selected_tower.deconstruct_button.click(mouse_pos) :
                        tower_info[selected_tower.pos.y][selected_tower.pos.x] = 0
                        towers.remove(selected_tower)
                        natural_ingot += 80
                        

                if not sending_wave and sent_next_wave_button.click(mouse_pos) :
                    give_bonus_time -= (send_next_wave - game_timer) * 1.2
                    send_next_wave = game_timer
                selected_tile, show_buy_tower, show_tower_info, selected_tower = select_tile(
                    mouse_pos, tower_info, towers, 
                    level_info['map'], show_tower_info, 
                    selected_tile, selected_tower
                )

                if setting_button.click(mouse_pos) :
                    setting()
                    time_previous = pygame.time.get_ticks()


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
        if boss != None :
            boss.display(screen)
        if not sending_wave :
            sent_next_wave_button.display(screen)
        setting_button.display(screen)
        show_text(
            'Next wave in {:.2f} s.'.format((send_next_wave - game_timer)/1000), 
            790, 545, (0, 0, 0), 20
        )
        show_text(
            'Wave : {}'.format(wave), 
            790, 570, (0, 0, 0), 20
        )
        
        natural_ingot_button.display(screen)
        show_text(str(math.floor(natural_ingot)), 850, 40, (0, 0, 0), 20)
        # bonus
        give_bonus_bar.display(screen)
        bonus_bar_image = pygame.transform.scale(
            give_bonus_bar.images[1], 
            (give_bonus_bar.width * (max(0, give_bonus_time) / give_bonus_wait_time), give_bonus_bar.width)
        )
        screen.blit(
            bonus_bar_image, 
            give_bonus_bar.pos.get_tuple()
        )
        

        hit_button.display(screen)
        show_text(str(hit), 850, 72, (0, 0, 0), 20)

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
        
        if not show_tower_info and not show_buy_tower :
            for en in enemy_types :
                en.display(screen)
            shift_pos = 80
            for i in range(ENEMY_TYPE) :
                show_text(
                    'Hit : {:.1f}'.format(
                    enemy_base_info[i][0][0] + enemy_base_info[i][1][0] * 
                    (enemy_level[i]**2)), 840, 140 + shift_pos * i, 
                    [0, 0, 0], 20
                )
                show_text(
                    'Shield : {:.1f}'.format(
                    enemy_base_info[i][0][2] + enemy_base_info[i][1][2] * 
                    (enemy_level[i]**2)), 840, 165 + shift_pos * i, 
                    [0, 0, 0], 20
                )
                show_text(
                    'Armor : {:.1f}'.format(
                    enemy_base_info[i][0][1] + enemy_base_info[i][1][1] * 
                    math.sqrt(enemy_level[i])), 840, 190 + shift_pos * i, 
                    [0, 0, 0], 20
                )

        display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
        pygame.display.update()

        clock.tick(FPS)
    if is_game_over :
        game_over()
    return

def level_editor() :
    levels_file = open(os.path.join(os.getcwd(), 'AppData', 'levels.json'), 'r')
    levels = levels_file.read()
    levels = json.loads(levels)
    levels_file.close()

    new_level_name = ''
    level_name_pos = 0

    title = 'Enter Level Name'
    level_name_button = button(
        "", vec2D(resolution[0]/2 - 256, resolution[1]/2 - 32), 
        [0, 0, 0], 512, 64, ['select_level.png']
    )

    # enter level name
    in_game = True
    file_name_exist = False
    while in_game :
        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    return
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN :
                    for file_name in levels['file_name'] :
                        if file_name == new_level_name :
                            file_name_exist = True
                    if not file_name_exist and new_level_name != '' :
                        in_game = False
                elif event.key == pygame.K_BACKSPACE :
                    if level_name_pos > 0 :
                        new_level_name = new_level_name[:level_name_pos - 1] + new_level_name[level_name_pos:]
                    level_name_pos = max(0, level_name_pos - 1)
                elif event.key == pygame.K_DELETE :
                    if level_name_pos < len(new_level_name) :
                        new_level_name = new_level_name[:level_name_pos] + new_level_name[level_name_pos + 1:]
                elif event.key == pygame.K_LEFT :
                    level_name_pos = max(0, level_name_pos - 1)
                elif event.key == pygame.K_RIGHT :
                    level_name_pos = min(level_name_pos + 1, len(new_level_name))
                elif event.key == pygame.K_UP :
                    level_name_pos = 0
                elif event.key == pygame.K_DOWN :
                    level_name_pos = len(new_level_name)
                elif event.key == pygame.K_LSHIFT :
                    a = 0
                else :
                    if level_name_pos >= 15 :
                        continue
                    if(
                        (event.key >= pygame.K_a and event.key <= pygame.K_z) or 
                        event.unicode.isdigit() or
                        event.unicode == chr(pygame.K_UNDERSCORE)
                    ) :
                        new_level_name = new_level_name[:level_name_pos] + event.unicode + new_level_name[level_name_pos:]
                        level_name_pos += 1
                
        
        # display
        screen.fill((245, 245, 245))

        level_name_button.display(screen)
        show_text(title, 250, 180, (0, 0, 0), 72)
        show_text(new_level_name, 280, 270, (0, 0, 0), 64)
        show_text('|', 262 + level_name_pos * 32, 270, (0, 0, 0), 64)
        if file_name_exist :
            show_text('File Name Exists', 262, 350, (255, 50, 50), 64)
        display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)

    new_level_name += '.json'

    # level editor
    tile_set = tile.tileset([
        'white.png',
        'main_tower.png',
        'enemy_sourse.png',
        'road.png'
    ], 64, 64)
    
    level_info = {
        'map_size' : [9, 12], "difficulty" : 100,
        "start_wave" : 0, "start_money" : 150,
        "start_hit" : 20
    }

    map_info = []
    for i in range(9) :
        line = []
        for j in range(12) :
            line.append(0)
        map_info.append(line)
    level_info['map'] = map_info

    level_map = tile.tilemap(tile_set, [9, 12])
    def update_map(level_map = tile.tilemap(tile_set, [12, 9])) :
        level_map.set_zero()
        level_map.load(map_info)
        level_map.render()
    update_map(level_map)
        
    # level_path = find_path(map_info)

    time_previous = pygame.time.get_ticks()
    game_timer = 0

    # row col -> y, x
    selected_tile = [0, 0]

    def editor_select_tile(mouse_pos = vec2D(0, 0)) :
        selected_tile = None
        tile_pos = [mouse_pos.y // 64, mouse_pos.x // 64]

        if(
            tile_pos[0] < 9 and 
            tile_pos[1] < 12
        ) :
            selected_tile = tile_pos
        return selected_tile

    tile_rect = pygame.Rect([0, 0], [tile.TILE_SIZE, tile.TILE_SIZE])

    # buy tower button
    show_tiles = False
    tile_buttons = [
        button(
            0, vec2D(785, 80), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'white.png'], 
        ),

        button(
            0, vec2D(845, 80), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'main_tower.png'], 
        ),

        button(
            0, vec2D(905, 80), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'enemy_sourse.png'], 
        ),

        button(
            0, vec2D(785, 140), 
            [0, 0, 0], 64, 64, 
            ['can_buy_tower.png', 'road.png'], 
        ),
    ]

    for tl in tile_buttons :
        tl.images[1] = pygame.transform.scale(tl.images[1], [48, 48])

    input_buttons = []
    input_button_text = [
        'difficulty', 
        'start_wave', 
        'start_money',
        'start_hit'
    ]

    shift_pos = 60
    for i in range(4) :
        input_buttons.append(
            button(
                input_button_text[i], vec2D(780, 110 + shift_pos * i), 
                [0, 0, 0], 200, 25, ['select_level.png']
            )
        )

    buffer_string = ''
    selected_input = None
    level_name_pos = 0

    save_button = button(
        'save', vec2D(775, 490), 
        [0, 0, 0], 32, 32, 
        ['save_button.png']
    )

    def save() :
        path = find_path(map_info)
        if path == None :
            return False
        level_info['map'] = map_info
        try :
            output = open(os.path.join(os.getcwd(), 'AppData', new_level_name), 'x')
            output.write(json.dumps(level_info))
            output.close()
            input_levels = open(os.path.join(os.getcwd(), 'AppData', 'levels.json'), 'r')
            input = input_levels.read()
            input = json.loads(input)
            output = open(os.path.join(os.getcwd(), 'AppData', 'levels.json'), 'w')
            input['file_name'].append(new_level_name[:-5])
            output.write(json.dumps(input))
            output.close()
        except :
            output = open(os.path.join(os.getcwd(), 'AppData', new_level_name), 'w')
            output.write(json.dumps(level_info))
            output.close()
        return True

    is_error = False
    error_reset_time = 1000

    in_game = True
    while in_game :
        time_now = pygame.time.get_ticks()
        delta_time = time_now - time_previous
        time_previous = time_now
        game_timer += delta_time

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2D(mouse_pos[0],mouse_pos[1])

        if error_reset_time > 0 :
            error_reset_time -= delta_time
        else :
            is_error = False

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                # difficulty
                # start_wave
                # start_money
                # start_hit
                if event.key == pygame.K_ESCAPE :
                    in_game = False
                elif event.key == pygame.K_BACKSPACE :
                    if level_name_pos > 0 :
                        buffer_string = buffer_string[:level_name_pos - 1] + buffer_string[level_name_pos:]
                    level_name_pos = max(0, level_name_pos - 1)
                elif event.key == pygame.K_DELETE :
                    if level_name_pos < len(buffer_string) :
                        buffer_string = buffer_string[:level_name_pos] + buffer_string[level_name_pos + 1:]
                elif event.key == pygame.K_LEFT :
                    level_name_pos = max(0, level_name_pos - 1)
                elif event.key == pygame.K_RIGHT :
                    level_name_pos = min(level_name_pos + 1, len(buffer_string))
                elif event.key == pygame.K_UP :
                    level_name_pos = 0
                elif event.key == pygame.K_DOWN :
                    level_name_pos = len(buffer_string)
                elif event.key == pygame.K_LSHIFT :
                    a = 0
                else :
                    if level_name_pos >= 18 :
                        continue
                    if event.unicode.isdigit() :
                        buffer_string = buffer_string[:level_name_pos] + event.unicode + buffer_string[level_name_pos:]
                        level_name_pos += 1
                if selected_input != None :
                    if buffer_string == '' :
                        buffer_string = '0'
                    level_info[selected_input] = int(buffer_string)
            if event.type == pygame.MOUSEBUTTONDOWN : 
                mouse = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP and mouse[0] :
                mouse = [False, False, False]
                if save_button.click(mouse_pos) :
                    if not save() :
                        error_reset_time = 1000
                        is_error = True
                
                ct = 0
                for tl in tile_buttons :
                    if(
                        show_tiles and 
                        tl.click(mouse_pos)
                    ) :
                        map_info[selected_tile[0]][selected_tile[1]] = ct
                        update_map(level_map)
                    ct += 1
                selected_tile = editor_select_tile(mouse_pos)
                if selected_tile == None :
                    show_tiles = False
                else :
                    show_tiles = True
                is_click = False
                for btn in input_buttons :
                    if (not show_tiles) and btn.click(mouse_pos) :
                        selected_input = btn.text
                        buffer_string = str(level_info[btn.text])
                        level_name_pos = len(buffer_string)
                        is_click = True
                if not is_click :
                    selected_input = None
                


        # display
        screen.fill((245, 245, 245))
        screen.blit(level_map.image, level_map.rect)

        if show_tiles :
            tile_rect.center = transform(
                vec2D(selected_tile[1], selected_tile[0]), 
                tile.TILE_SIZE
            ).get_tuple()
            color = pygame.Color(100, 120, 180, a=100)
            pygame.draw.rect(
                screen, color, 
                tile_rect, 0
            )
        
        if show_tiles :
            for tl in tile_buttons :
                tl.state = 0
                tl.display(screen)
                screen.blit(tl.images[1], (tl.pos + vec2D(8, 8)).get_tuple())
        else :
            i = 0
            for btn in input_buttons :
                btn.display(screen)
            for btn in input_buttons :
                if selected_input == btn.text :
                    break
                i += 1
            

            show_text(
                'Difficulty', 
                790, 100, [0, 0, 0], 20
            )
            show_text(
                str(level_info['difficulty']), 
                795, 130, [0, 0, 0], 20
            )

            show_text(
                'Initial Wave', 
                790, 160, [0, 0, 0], 20
            )
            show_text(
                str(level_info['start_wave']), 
                795, 190, [0, 0, 0], 20
            )

            show_text(
                'Initial Natural Ingot', 
                790, 220, [0, 0, 0], 20
            )
            show_text(
                str(level_info['start_money']), 
                795, 250, [0, 0, 0], 20
            )

            show_text(
                'Initial Hit', 
                790, 280, [0, 0, 0], 20
            )
            show_text(
                str(level_info['start_hit']), 
                795, 310, [0, 0, 0], 20
            )

            if selected_input != None :
                show_text(
                    '|', 791 + 10 * level_name_pos, 
                    130 + shift_pos * i, (0, 0, 0), 20
                )
        save_button.display(screen)
        
        if is_error :
            show_text('Error', 300, 175, (0, 0, 0), 108)

        display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
        pygame.display.update()

        clock.tick(FPS)

    save()
    return

def select_level() :
    levels_file = open(os.path.join(os.getcwd(), 'AppData', 'levels.json'), 'r')
    levels = levels_file.read()
    levels = json.loads(levels)
    levels_file.close()

    select_level_button = []
    level_per_page = levels['level_per_page']
    shift_pos = 70
    for i in range(level_per_page) :
        select_level_button.append(
            button(
                "", vec2D(resolution[0]/2 - 256, 130 + shift_pos * i), 
                [0, 0, 0], 512, 64, ['select_level.png']
            )
        )
    page = 0
    max_page = len(levels['file_name']) // level_per_page + 1
    level_num = len(levels['file_name'])
    next_page_button = button(
        "", vec2D(resolution[0]/2 + 256 - 128, 130 + shift_pos * level_per_page), 
        [0, 0, 0], 64, 64, ['next_page_button.png']
    )
    prev_page_button = button(
        "", vec2D(resolution[0]/2 - 256 + 64, 130 + shift_pos * level_per_page), 
        [0, 0, 0], 64, 64, ['next_page_button.png']
    )
    prev_page_button.images[0] = pygame.transform.flip(prev_page_button.images[0], True, False)

    
    title = 'Select Level'

    in_game=True
    while in_game :
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2D(mouse_pos[0], mouse_pos[1])

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                # start_button.detect(pos = mouse_pos)
                mouse = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP and mouse[0] :
                mouse = [False, False, False]
                if next_page_button.click(mouse_pos) :
                    page = (page + 1) % max_page
                elif prev_page_button.click(mouse_pos) :
                    page = (page - 1 + max_page) % max_page
                idx = 0
                for btn in select_level_button :
                    if btn.click(mouse_pos) :
                        level(levels['file_name'][idx + (page * level_per_page)] + '.json')
                        return
                    idx += 1
                
        
        # display
        screen.fill((245, 245, 245))
        idx = 0
        for btn in select_level_button :
            if level_num <= idx + (page * level_per_page) :
                break
            btn.display(screen)
            show_text(
                levels['file_name'][idx + (page * level_per_page)], 
                300, 163 + shift_pos * idx, (0, 0, 0), 36
            )
            idx += 1

        next_page_button.display(screen)
        prev_page_button.display(screen)
        show_text(title, 300, 48, (0, 0, 0), 72)
        show_text(
            '{} / {}'.format(page + 1, max_page), 
            500, 525, (0, 0, 0), 20
        )
        display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    return


def main_page() :
    global is_fullscreen, volume
    input_file = open(os.path.join(os.getcwd(), 'AppData', 'setting.json'), 'r')
    input = input_file.read()
    input = json.loads(input)
    input_file.close()

    is_fullscreen = input['is_fullscreen']
    volume = input['volume']

    if is_fullscreen :
        flags = DOUBLEBUF | SCALED | FULLSCREEN
    else :
        flags = DOUBLEBUF
    display = pygame.display.set_mode(resolution, flags, 32)

    def click_start_button() :
        return True
    start_button = button('Start', vec2D(resolution[0]/2-64, resolution[1]/2-64), 
                          [0, 0, 0], 128, 128, 
                          ['start_button.png'], click_start_button)
    start_button.pos = vec2D(
        resolution[0] / 2 - start_button.width / 2, 
        resolution[1] / 2 - start_button.height / 2 + 50)
    setting_button = button('setting', vec2D(resolution[0]/2-64, resolution[1]/2-64), 
                          [0, 0, 0], 128, 128, 
                          ['setting_button.png'], click_start_button)
    setting_button.pos = vec2D(
        (resolution[0] / 2) - setting_button.width / 2 + 150, 
        (resolution[1] / 2) - setting_button.height / 2 + 50)
    level_editor_button = button('setting', vec2D(resolution[0]/2-64, resolution[1]/2-64), 
                          [0, 0, 0], 128, 128, 
                          ['level_editor_button.png'], click_start_button)
    level_editor_button.pos = vec2D(
        (resolution[0] / 2) - level_editor_button.width / 2 - 150, 
        (resolution[1] / 2) - level_editor_button.height / 2 + 50)
    
    
    title = 'Basic TD'

    in_game=True
    while in_game :
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2D(mouse_pos[0], mouse_pos[1])

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN : 
                start_button.detect(pos = mouse_pos)
                setting_button.detect(mouse_pos)
            if event.type == pygame.MOUSEBUTTONUP :
                if start_button.click(mouse_pos) :
                    select_level()
                elif setting_button.click(mouse_pos) :
                    setting()
                elif level_editor_button.click(mouse_pos) :
                    level_editor()
        
        # display
        screen.fill((245, 245, 245))
        start_button.display(screen)
        setting_button.display(screen)
        level_editor_button.display(screen)
        show_text(title, 300, 175, (0, 0, 0), 108)
        display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    return

main_page()
pygame.quit()