from src import tile
import os
import json
from src.util import *
import pygame
from src.enemy import *
import math
from src.button import button
from src.variables import *
from src.tower import *
from src.scene import *
import numpy as np


def load_level_info(level_name):
    tile_set = tile.tileset([
        'white.png',
        'main_tower.png',
        'enemy_sourse.png',
        'road.png'
    ], 64, 64)
    level_info_file = open(os.path.join(
        os.getcwd(), 'AppData', level_name), 'r')
    level_info = level_info_file.read()
    level_info = json.loads(level_info)
    level_info_file.close()
    return tile_set, level_info


def init_enemy_base_info(difficulty):
    return [
        [[30*difficulty/100,  0,  0,  30, 300],
            [1.5*difficulty/100,    0,    0,   1, 30]],
        [[10*difficulty/100,  5, 20,  40, 300],
            [0.1*difficulty/100, 0.05,  1.4,   1, 30]],
        [[30*difficulty/100, 10,  1,  25, 300],
            [5*difficulty/100,    1, 0.05, 0.1, 30]],
    ]


def init_buy_tower_buttons():
    return [
        button(
            80, pygame.Vector2(785, 80),
            [0, 0, 0], 64, 64,
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'basic_tower32.png']
        ),

        button(
            150, pygame.Vector2(845, 80),
            [0, 0, 0], 64, 64,
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'sniper_tower32.png']
        ),

        button(
            300, pygame.Vector2(905, 80),
            [0, 0, 0], 64, 64,
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'cannon_tower32.png']
        ),

        button(
            400, pygame.Vector2(785, 140),
            [0, 0, 0], 64, 64,
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'tesla_tower32.png']
        ),

        button(
            10000, pygame.Vector2(845, 140),
            [0, 0, 0], 64, 64,
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'acid_tower64.png']
        ),

        button(
            50000, pygame.Vector2(905, 140),
            [0, 0, 0], 64, 64,
            ['can_buy_tower.png', 'cannot_buy_tower.png', 'spread_tower64.png'],
        ),
    ]


def init_buy_tower_info():
    return [
        [
            'Basic',
            'Basic tower can attack',
            'fast, and it\'s cheap.'
        ],

        [
            'Sniper',
            'Sniper Tower attack ',
            'slowly. However, it\'s ',
            'a good way to break',
            'the armor.'
        ],

        [
            'Cannon',
            'Cannon Tower provides AOE',
            'damage, and has greatest',
            'DPS. Also, it can damage ',
            'though shield.'
        ],

        [
            'Tesla',
            'Tesla Tower can damage all ',
            'enemys with in range, and ',
            'interfer the shield ',
            'regeneration.'
        ],

        [
            'Acid',
            'Acid can make the enemy ',
            'miss the direction and ',
            'go backward on the track.'
        ],

        [
            'Split',
            'Split can shoot special ',
            'bullet which is able to ',
            'split multiple times, ',
            'depending on it\'s layer.'
        ],
    ]


def enhance_enemy(wave, enemy_base_info, enemy_types, boss_types, enemy_level):
    # Enhance Enemy
    if wave >= 100:
        # make basic enemy much stronger
        enemy_base_info[0][1][0] = 15
        enemy_base_info[0][1][3] = 3
        enemy_base_info[0][0][3] = 60
        enemy_base_info[0][0][4] = 150
        enemy_types[0] = angry_basic(
            enemy_types[0].pos, 0, 0, 0, 10, [enemy_types[0].pos])
        enemy_types[0].location = enemy_types[0].pos
    if wave >= 125:
        enemy_base_info[1][1][0] = 2.5
        enemy_base_info[1][1][1] = 1.25
        enemy_base_info[1][1][2] = 35
        enemy_base_info[1][1][3] = 15
        enemy_base_info[1][0][3] = 80
        enemy_base_info[1][0][4] = 135
        enemy_types[1] = chaos_eye(
            enemy_types[1].location, 0, 0, 0, 10, [enemy_types[1].pos])
        enemy_types[1].location = enemy_types[1].pos
    if wave >= 150:
        enemy_base_info[2][1][0] = 100
        enemy_base_info[2][1][1] = 40
        enemy_base_info[2][1][2] = 3
        enemy_base_info[2][1][3] = 1.5
        enemy_base_info[2][0][3] = 50
        enemy_base_info[2][0][4] = 150
        enemy_types[2] = super_shield(
            enemy_types[2].pos, 0, 0, 0, 10, [enemy_types[2].pos])
        enemy_types[2].location = enemy_types[2].pos
    if wave >= 200:
        # make basic enemy much stronger
        enemy_base_info[0][1][0] = 300
        enemy_base_info[0][1][1] = 0.01
        enemy_base_info[0][1][2] = 0.01
        enemy_base_info[0][1][3] = 75
        enemy_base_info[0][0][3] = 100
        enemy_base_info[0][0][4] = 100
        enemy_types[0] = shielded_basic(
            enemy_types[0].pos, 0, 0, 0, 10, [enemy_types[0].pos])
        enemy_types[0].location = enemy_types[0].pos
        boss_types[0] = shielded_basic_boss(
            enemy_types[0].pos, 0, 0, 0, 20, [enemy_types[0].pos])
    if wave >= 225:
        enemy_base_info[1][1][0] = 25
        enemy_base_info[1][1][1] = 12.5
        enemy_base_info[1][1][2] = 350
        enemy_base_info[1][1][3] = 75
        enemy_base_info[1][0][3] = 120
        enemy_base_info[1][0][4] = 80
        enemy_types[1] = storm_eye(
            enemy_types[1].location, 0, 0, 0, 10, [enemy_types[1].pos])
        enemy_types[1].location = enemy_types[1].pos
        boss_types[1] = storm_eye_boss(
            enemy_types[1].location, 0, 0, 0, 20, [enemy_types[1].pos])
    if wave >= 250:
        enemy_base_info[2][1][0] = 1000
        enemy_base_info[2][1][1] = 400
        enemy_base_info[2][1][2] = 30
        enemy_base_info[2][1][3] = 15
        enemy_base_info[2][0][3] = 80
        enemy_base_info[2][0][4] = 100
        enemy_types[2] = ultra_shield(
            enemy_types[2].pos, 0, 0, 0, 10, [enemy_types[2].pos])
        enemy_types[2].location = enemy_types[2].pos
        boss_types[2] = ultra_high_armor_boss(
            enemy_types[2].pos, 0, 0, 0, 20, [enemy_types[2].pos])
    if wave >= 300:
        idx = 0
        for lv in enemy_level:
            enemy_base_info[idx][0][4] = 50
            enemy_base_info[idx][0][3] += 5
            enemy_level[idx] += 30
            idx += 1


def send_boss(wave, boss, boss_level, boss_types, enemy_base_info, enemy_level, level_path, difficulty):
    if wave >= 250:
        idx = 0
        for lv in enemy_level:
            enemy_level[idx] += math.sqrt(wave)
            enemy_base_info[idx][1][3] += 10
            idx += 1
    if boss != None:
        boss_level += 3
        return True
    enemy_type_this_wave = boss_level % 3
    boss_level += 1
    boss = boss_types[enemy_type_this_wave].copy()
    base_hit = enemy_base_info[enemy_type_this_wave][0][0] + \
        enemy_base_info[enemy_type_this_wave][1][0] * \
        (enemy_level[enemy_type_this_wave]**2)
    base_armor = enemy_base_info[enemy_type_this_wave][0][1] + \
        enemy_base_info[enemy_type_this_wave][1][1] * \
        math.sqrt(enemy_level[enemy_type_this_wave])
    base_shield = enemy_base_info[enemy_type_this_wave][0][2] + \
        enemy_base_info[enemy_type_this_wave][1][2] * \
        (enemy_level[enemy_type_this_wave]**2)
    boss.__init__(
        level_path[0].copy(),
        base_hit * (difficulty / 100) * 10 * (boss_level ** 2),
        base_armor * (difficulty / 100) * 10 * boss_level,
        base_shield * (difficulty / 100) *
        10 * (boss_level ** 2),
        boss.move_speed, level_path
    )
    return boss, boss_level, False


def level(screen, display, level_name='basic_level.json'):
    tile_set, level_info = load_level_info(level_name)

    level_map = tile.tilemap(tile_set, level_info['map_size'])
    level_map.set_zero()
    level_map.load(level_info['map'])
    level_map.render()
    level_path = find_path(level_info['map'])

    towers = []
    tower_info = np.zeros(level_info['map_size'], dtype=int)
    show_tower_info = False
    selected_tower = None

    enemys = []

    enemy_types = init_enemy_types(level_path)
    ENEMY_TYPE = len(enemy_types)

    for en in enemy_types:
        en.location = en.pos
    enemy_level = [0, 0, 5]

    enemy_base_info = init_enemy_base_info(level_info['difficulty'])

    boss_types = init_boss_types()
    boss = None

    enemy_type_this_wave = 0
    enemy_type_next_wave = 0

    time_previous = pygame.time.get_ticks()
    game_timer = 0

    wave = level_info['start_wave']
    boss_level = max(0, (wave - 100) // 25)
    for i in range(ENEMY_TYPE):
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
        'Natural Ingot', pygame.Vector2(785, 16),
        [0, 0, 0], 32, 32, ['natural_ingot16.png']
    )

    # bonus
    give_bonus_rate = 0.05
    give_bonus_wait_time = 20000
    give_bonus_time = give_bonus_wait_time
    give_bonus_bar = button(
        'Give_Bonus_Bar', pygame.Vector2(945, 6),
        [0, 0, 0], 48, 48, ['hit_bar_red.png', 'hit_bar_blue.png']
    )

    # player health
    hit = level_info['start_hit']
    hit_button = button(
        'Player Health', pygame.Vector2(785, 48),
        [0, 0, 0], 32, 32, ['main_tower.png']
    )

    # row col -> y, x
    selected_tile = [0, 0]

    tile_rect = pygame.Rect([0, 0], [tile.TILE_SIZE, tile.TILE_SIZE])

    difficulty = level_info['difficulty']

    # buy tower button
    show_buy_tower = False

    buy_tower_buttons = init_buy_tower_buttons()
    buy_tower_info = init_buy_tower_info()

    # sent next wave
    sent_next_wave_button = button(
        'sent_next_wave', pygame.Vector2(775, 490),
        [0, 0, 0], 32, 32,
        ['start_button.png']
    )

    setting_button = button(
        'setting', pygame.Vector2(835, 490),
        [0, 0, 0], 32, 32,
        ['setting_button.png']
    )

    is_game_over = False
    is_sending_boss = False

    # Enhance Enemy
    enhance_enemy(wave, enemy_base_info, enemy_types, boss_types, enemy_level)

    # global volume
    mouse = [False, False, False]

    in_game = True
    while in_game:
        time_now = pygame.time.get_ticks()
        delta_time = time_now - time_previous

        # delta_time *= 0.25

        time_previous = time_now
        game_timer += delta_time

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = pygame.Vector2(mouse_pos[0], mouse_pos[1])

        if game_timer > send_next_wave:
            wave += 1
            enhance_enemy(wave, enemy_base_info, enemy_types,
                          boss_types, enemy_level)
            if (wave >= 100 and wave % 25 == 0) or is_sending_boss:
                boss, boss_level, is_sending_boss = send_boss(
                    wave, boss, boss_level, boss_types, enemy_base_info, enemy_level, level_path, difficulty)

            # Generate Enemy
            enemy_type_this_wave = enemy_type_next_wave
            enemy_level[enemy_type_this_wave] += 1
            send_this_wave = send_next_wave
            enemy_type_next_wave = random.randint(
                0, min(math.floor(wave / 5), ENEMY_TYPE - 1))
            enemy_amount = math.floor(
                math.sqrt(
                    enemy_level[enemy_type_this_wave] *
                    enemy_base_info[enemy_type_this_wave][1][3]
                )
            ) + 1
            enemy_dencity = max(
                enemy_base_info[enemy_type_this_wave][0][4],
                1000-enemy_base_info[enemy_type_this_wave][1][4] *
                enemy_level[enemy_type_this_wave]
            )
            wave_interval = math.ceil(
                enemy_amount * enemy_dencity) + random.randint(10000, 25000)
            send_next_wave += wave_interval
            sending_wave = True
            sent_enemy += enemy_amount
            send_next_enemy = 0

        if sending_wave and game_timer >= send_next_enemy+send_this_wave:
            send_next_enemy += enemy_dencity
            nen = enemy_types[enemy_type_this_wave].copy()
            base_hit = enemy_base_info[enemy_type_this_wave][0][0] + \
                enemy_base_info[enemy_type_this_wave][1][0] * \
                (enemy_level[enemy_type_this_wave]**2)
            base_armor = enemy_base_info[enemy_type_this_wave][0][1] + \
                enemy_base_info[enemy_type_this_wave][1][1] * \
                math.sqrt(enemy_level[enemy_type_this_wave])
            base_shield = enemy_base_info[enemy_type_this_wave][0][2] + \
                enemy_base_info[enemy_type_this_wave][1][2] * \
                (enemy_level[enemy_type_this_wave]**2)
            nen.__init__(
                level_path[0].copy(),
                base_hit * difficulty / 100,
                base_armor * difficulty / 100,
                base_shield * difficulty / 100,
                enemy_base_info[enemy_type_this_wave][0][3], level_path
            )
            enemys.append(nen)
            sent_enemy -= 1
            if sent_enemy == 0:
                sending_wave = False

        for tow in towers:
            tow.update(delta_time, enemys, boss)
        for en in enemys:
            if en.update(delta_time):
                hit -= 1
                if hit <= 0:
                    is_game_over = True
                    in_game = False
            if not en.alive:
                enemys.remove(en)
                natural_ingot += math.sqrt(en.max_hit + en.max_shield)
        if boss != None:
            if boss.update(delta_time):
                hit -= 1
                boss.pos = boss.location = level_path[0].copy()
                boss.progress = 0
                if hit <= 0:
                    is_game_over = True
                    in_game = False
            for en in boss.generated_unit:
                if en.update(delta_time):
                    hit -= 1
                    if hit <= 0:
                        is_game_over = True
                        in_game = False
                if not en.alive:
                    boss.generated_unit.remove(en)
            if boss.dead:
                natural_ingot += math.sqrt(boss.max_hit + boss.max_shield)
                boss = None

        if give_bonus_time > 0:
            give_bonus_time -= delta_time
        else:
            give_bonus_time += give_bonus_wait_time
            natural_ingot += min(6000000, natural_ingot * give_bonus_rate)

        # event in pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()

            if event.type == pygame.MOUSEBUTTONUP and mouse[0]:

                ct = 1
                for buy_tower in buy_tower_buttons:
                    if (
                        show_buy_tower and
                        buy_tower.click(mouse_pos) and
                        buy_tower.text <= natural_ingot
                    ):
                        natural_ingot -= buy_tower.text
                        tower_info[selected_tile[0], selected_tile[1]] = ct
                        new_tower = None
                        if ct == 1:
                            new_tower = basic_tower(
                                pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                        elif ct == 2:
                            new_tower = sniper_tower(
                                pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                        elif ct == 3:
                            new_tower = cannon_tower(
                                pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                        elif ct == 4:
                            new_tower = tesla_tower(
                                pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                        elif ct == 5:
                            new_tower = acid_tower(
                                pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                        elif ct == 6:
                            new_tower = spread_tower(
                                pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                        new_tower.place(
                            pygame.Vector2(selected_tile[1], selected_tile[0]))
                        towers.append(new_tower)
                        break
                    ct += 1

                if selected_tower != None:
                    clicked_upgrade, natural_ingot = selected_tower.upgrade(
                        mouse_pos, natural_ingot
                    )
                    if clicked_upgrade:
                        continue
                    if selected_tower.deconstruct_button.click(mouse_pos):
                        tower_info[int(selected_tower.pos.y)
                                   ][int(selected_tower.pos.x)] = 0
                        towers.remove(selected_tower)
                        natural_ingot += 80
                        selected_tower = None
                        show_tower_info = False

                if not sending_wave and sent_next_wave_button.click(mouse_pos):
                    give_bonus_time -= (send_next_wave - game_timer) * 1.2
                    send_next_wave = game_timer
                selected_tile, show_buy_tower, show_tower_info, selected_tower = select_tile(
                    mouse_pos, tower_info, towers,
                    level_info['map'], show_tower_info,
                    selected_tile, selected_tower
                )

                if setting_button.click(mouse_pos):
                    setting(screen, display)
                    time_previous = pygame.time.get_ticks()
                    for tow in towers:
                        tow.volume = volume
                        tow.fire_sound.set_volume(tow.volume / 100)
                        if tow.explode_sound != None:
                            tow.explode_sound.set_volume(tow.volume / 100)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = [False, False, False]

        if mouse[2]:
            if selected_tower != None:
                clicked_upgrade, natural_ingot = selected_tower.upgrade(
                    mouse_pos, natural_ingot
                )

        # display
        screen.fill((245, 245, 245))
        screen.blit(level_map.image, level_map.rect)

        if show_buy_tower or show_tower_info:
            tile_rect.center = transform(
                pygame.Vector2(selected_tile[1], selected_tile[0]),
                tile.TILE_SIZE
            )
            color = pygame.Color(100, 120, 180, a=2)
            pygame.draw.rect(
                screen, color,
                tile_rect, 0
            )

        for tow in towers:
            tow.display(screen)
        for tow in towers:
            tow.display_bullets(screen)
        for en in enemys:
            en.display(screen)
        if boss != None:
            boss.display(screen)
        if not sending_wave:
            sent_next_wave_button.display(screen)
        setting_button.display(screen)
        show_text(
            screen,
            'Next wave in {:.2f} s.'.format(
                (send_next_wave - game_timer)/1000),
            790, 545, (0, 0, 0), 20
        )
        show_text(
            screen,
            'Wave : {}'.format(wave),
            790, 570, (0, 0, 0), 20
        )

        natural_ingot_button.display(screen)
        show_text(screen, str(math.floor(natural_ingot)),
                  850, 40, (0, 0, 0), 20)
        # bonus
        give_bonus_bar.display(screen)
        bonus_bar_image = pygame.transform.scale(
            give_bonus_bar.images[1],
            (give_bonus_bar.width * (max(0, give_bonus_time) /
             give_bonus_wait_time), give_bonus_bar.width)
        )
        screen.blit(
            bonus_bar_image,
            give_bonus_bar.pos
        )

        hit_button.display(screen)
        show_text(screen, str(hit), 850, 72, (0, 0, 0), 20)

        if show_buy_tower:
            ct = 0
            for buy_tower in buy_tower_buttons:
                if buy_tower.text > natural_ingot:
                    buy_tower.state = 1
                    buy_tower.display(screen)
                else:
                    buy_tower.state = 0
                    buy_tower.display(screen)
                buy_tower.state = 2
                buy_tower.display(screen)

                if buy_tower.click(mouse_pos):
                    idx = 0
                    line_buf = 25
                    for line in buy_tower_info[ct]:
                        show_text(
                            screen,
                            line, 790, 300 + line_buf * idx,
                            [0, 0, 0], 20
                        )
                        idx += 1
                    new_tower = None
                    if ct == 0:
                        new_tower = basic_tower(
                            pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                    elif ct == 1:
                        new_tower = sniper_tower(
                            pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                    elif ct == 2:
                        new_tower = cannon_tower(
                            pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                    elif ct == 3:
                        new_tower = tesla_tower(
                            pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                    elif ct == 4:
                        new_tower = acid_tower(
                            pygame.Vector2(selected_tile[1], selected_tile[0]), volume)
                    elif ct == 5:
                        new_tower = spread_tower(
                            pygame.Vector2(selected_tile[1], selected_tile[0]), volume)

                    pygame.draw.circle(
                        screen, [100, 200, 100], new_tower.location,
                        new_tower.range, 3
                    )

                ct += 1

        elif show_tower_info and selected_tower != None:
            color = pygame.Color(30, 30, 30, a=70)
            pygame.draw.circle(
                screen, color,
                selected_tower.location,
                selected_tower.range,
                3
            )

            selected_tower.display_info(screen, natural_ingot)

        if not show_tower_info:
            selected_tower = None

        if not show_tower_info and not show_buy_tower:
            for en in enemy_types:
                en.display(screen)
            shift_pos = 80
            for i in range(ENEMY_TYPE):
                show_text(
                    screen,
                    'Hit : {:.1f}'.format(
                        enemy_base_info[i][0][0] + enemy_base_info[i][1][0] *
                        (enemy_level[i]**2)), 840, 140 + shift_pos * i,
                    [0, 0, 0], 20
                )
                show_text(
                    screen,
                    'Shield : {:.1f}'.format(
                        enemy_base_info[i][0][2] + enemy_base_info[i][1][2] *
                        (enemy_level[i]**2)), 840, 165 + shift_pos * i,
                    [0, 0, 0], 20
                )
                show_text(
                    screen,
                    'Armor : {:.1f}'.format(
                        enemy_base_info[i][0][1] + enemy_base_info[i][1][1] *
                        math.sqrt(enemy_level[i])), 840, 190 + shift_pos * i,
                    [0, 0, 0], 20
                )

        display.blit(pygame.transform.scale(
            screen, display.get_size()), (0, 0))
        pygame.display.set_caption(f'Basic TD Game {clock.get_fps()}')
        pygame.display.update()

        clock.tick(FPS)
    if is_game_over:
        game_over(screen, display)
