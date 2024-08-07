import json
import os
from src.variables import *
from src.button import button
from src.util import *

def enter_level_name():
    levels_file = open(os.path.join(
        os.getcwd(), 'AppData', 'levels.json'), 'r')
    levels = levels_file.read()
    levels = json.loads(levels)
    levels_file.close()

    new_level_name = ''
    level_name_pos = 0

    title = 'Enter Level Name'
    level_name_button = button(
        "", pygame.Vector2(resolution[0]/2 - 256, resolution[1]/2 - 32),
        [0, 0, 0], 512, 64, ['select_level.png']
    )

    # enter level name
    in_game = True
    file_name_exist = False
    while in_game:
        # event in pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    for file_name in levels['file_name']:
                        if file_name == new_level_name:
                            file_name_exist = True
                    if not file_name_exist and new_level_name != '':
                        in_game = False
                elif event.key == pygame.K_BACKSPACE:
                    if level_name_pos > 0:
                        new_level_name = new_level_name[:level_name_pos -
                                                        1] + new_level_name[level_name_pos:]
                    level_name_pos = max(0, level_name_pos - 1)
                elif event.key == pygame.K_DELETE:
                    if level_name_pos < len(new_level_name):
                        new_level_name = new_level_name[:level_name_pos] + \
                            new_level_name[level_name_pos + 1:]
                elif event.key == pygame.K_LEFT:
                    level_name_pos = max(0, level_name_pos - 1)
                elif event.key == pygame.K_RIGHT:
                    level_name_pos = min(
                        level_name_pos + 1, len(new_level_name))
                elif event.key == pygame.K_UP:
                    level_name_pos = 0
                elif event.key == pygame.K_DOWN:
                    level_name_pos = len(new_level_name)
                elif event.key == pygame.K_LSHIFT:
                    a = 0
                else:
                    if level_name_pos >= 15:
                        continue
                    if (
                        (event.key >= pygame.K_a and event.key <= pygame.K_z) or
                        event.unicode.isdigit() or
                        event.unicode == chr(pygame.K_UNDERSCORE)
                    ):
                        new_level_name = new_level_name[:level_name_pos] + \
                            event.unicode + new_level_name[level_name_pos:]
                        level_name_pos += 1

        # display
        screen.fill((245, 245, 245))

        level_name_button.display(screen)
        show_text(screen, title, 250, 180, (0, 0, 0), 72)
        show_text(screen, new_level_name, 280, 270, (0, 0, 0), 64)
        show_text(screen, '|', 262 + level_name_pos * 32, 270, (0, 0, 0), 64)
        if file_name_exist:
            show_text(screen, 'File Name Exists', 262, 350, (255, 50, 50), 64)
        display.blit(pygame.transform.scale(
            screen, display.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    return new_level_name + '.json'

def save(map_info, level_info, new_level_name):
    path = find_path(map_info)
    if path == None:
        return False
    level_info['map'] = map_info
    try:
        output = open(os.path.join(
            os.getcwd(), 'AppData', new_level_name), 'x')
        output.write(json.dumps(level_info))
        output.close()
        input_levels = open(os.path.join(
            os.getcwd(), 'AppData', 'levels.json'), 'r')
        input = input_levels.read()
        input = json.loads(input)
        output = open(os.path.join(
            os.getcwd(), 'AppData', 'levels.json'), 'w')
        input['file_name'].append(new_level_name[:-5])
        output.write(json.dumps(input))
        output.close()
    except:
        output = open(os.path.join(
            os.getcwd(), 'AppData', new_level_name), 'w')
        output.write(json.dumps(level_info))
        output.close()
    return True

def update_map(level_map, map_info):
    level_map.set_zero()
    level_map.load(map_info)
    level_map.render()

def editor_select_tile(mouse_pos=pygame.Vector2(0, 0)):
    selected_tile = None
    tile_pos = [mouse_pos.y // 64, mouse_pos.x // 64]

    if tile_pos[0] < 9 and tile_pos[1] < 12:
        selected_tile = tile_pos
    return selected_tile

def level_editor(screen, display):
    new_level_name = enter_level_name()
    tile_set = tile.tileset([
        'white.png',
        'main_tower.png',
        'enemy_sourse.png',
        'road.png'
    ], 64, 64)

    level_info = {
        'map_size': [9, 12], "difficulty": 100,
        "start_wave": 0, "start_money": 150,
        "start_hit": 20
    }

    map_info = []
    for i in range(9):
        line = []
        for j in range(12):
            line.append(0)
        map_info.append(line)
    level_info['map'] = map_info

    level_map = tile.tilemap(tile_set, [9, 12])

    update_map(level_map, map_info)

    # level_path = find_path(map_info)

    time_previous = pygame.time.get_ticks()
    game_timer = 0

    # row col -> y, x
    selected_tile = [0, 0]

    tile_rect = pygame.Rect([0, 0], [tile.TILE_SIZE, tile.TILE_SIZE])

    # buy tower button
    show_tiles = False
    tile_buttons = [
        button(
            0, pygame.Vector2(785, 80),
            [0, 0, 0], 64, 64,
            ['can_buy_tower.png', 'white.png'],
        ),

        button(
            0, pygame.Vector2(845, 80),
            [0, 0, 0], 64, 64,
            ['can_buy_tower.png', 'main_tower.png'],
        ),

        button(
            0, pygame.Vector2(905, 80),
            [0, 0, 0], 64, 64,
            ['can_buy_tower.png', 'enemy_sourse.png'],
        ),

        button(
            0, pygame.Vector2(785, 140),
            [0, 0, 0], 64, 64,
            ['can_buy_tower.png', 'road.png'],
        ),
    ]

    for tl in tile_buttons:
        tl.images[1] = pygame.transform.scale(tl.images[1], [48, 48])

    input_buttons = []
    input_button_text = [
        'difficulty',
        'start_wave',
        'start_money',
        'start_hit'
    ]

    shift_pos = 60
    for i in range(4):
        input_buttons.append(
            button(
                input_button_text[i], pygame.Vector2(780, 110 + shift_pos * i),
                [0, 0, 0], 200, 25, ['select_level.png']
            )
        )

    buffer_string = ''
    selected_input = None
    level_name_pos = 0

    save_button = button(
        'save', pygame.Vector2(775, 490),
        [0, 0, 0], 32, 32,
        ['save_button.png']
    )

    is_error = False
    error_reset_time = 1000

    in_game = True
    while in_game:
        time_now = pygame.time.get_ticks()
        delta_time = time_now - time_previous
        time_previous = time_now
        game_timer += delta_time

        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = pygame.Vector2(mouse_pos[0], mouse_pos[1])

        if error_reset_time > 0:
            error_reset_time -= delta_time
        else:
            is_error = False

        # event in pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                # difficulty
                # start_wave
                # start_money
                # start_hit
                if event.key == pygame.K_ESCAPE:
                    in_game = False
                elif event.key == pygame.K_BACKSPACE:
                    if level_name_pos > 0:
                        buffer_string = buffer_string[:level_name_pos -
                                                      1] + buffer_string[level_name_pos:]
                    level_name_pos = max(0, level_name_pos - 1)
                elif event.key == pygame.K_DELETE:
                    if level_name_pos < len(buffer_string):
                        buffer_string = buffer_string[:level_name_pos] + \
                            buffer_string[level_name_pos + 1:]
                elif event.key == pygame.K_LEFT:
                    level_name_pos = max(0, level_name_pos - 1)
                elif event.key == pygame.K_RIGHT:
                    level_name_pos = min(
                        level_name_pos + 1, len(buffer_string))
                elif event.key == pygame.K_UP:
                    level_name_pos = 0
                elif event.key == pygame.K_DOWN:
                    level_name_pos = len(buffer_string)
                elif event.key == pygame.K_LSHIFT:
                    a = 0
                else:
                    if level_name_pos >= 18:
                        continue
                    if event.unicode.isdigit():
                        buffer_string = buffer_string[:level_name_pos] + \
                            event.unicode + buffer_string[level_name_pos:]
                        level_name_pos += 1
                if selected_input != None:
                    if buffer_string == '':
                        buffer_string = '0'
                    level_info[selected_input] = int(buffer_string)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP and mouse[0]:
                mouse = [False, False, False]
                if save_button.click(mouse_pos):
                    if not save(map_info, level_info, new_level_name):
                        error_reset_time = 1000
                        is_error = True

                ct = 0
                for tl in tile_buttons:
                    if (
                        show_tiles and
                        tl.click(mouse_pos)
                    ):
                        map_info[int(selected_tile[0])][int(selected_tile[1])] = ct
                        update_map(level_map, map_info)
                    ct += 1
                selected_tile = editor_select_tile(mouse_pos)
                if selected_tile == None:
                    show_tiles = False
                else:
                    show_tiles = True
                is_click = False
                for btn in input_buttons:
                    if (not show_tiles) and btn.click(mouse_pos):
                        selected_input = btn.text
                        buffer_string = str(level_info[btn.text])
                        level_name_pos = len(buffer_string)
                        is_click = True
                if not is_click:
                    selected_input = None

        # display
        screen.fill((245, 245, 245))
        screen.blit(level_map.image, level_map.rect)

        if show_tiles:
            tile_rect.center = transform(
                pygame.Vector2(selected_tile[1], selected_tile[0]),
                tile.TILE_SIZE
            )
            color = pygame.Color(100, 120, 180, a=100)
            pygame.draw.rect(
                screen, color,
                tile_rect, 0
            )

        if show_tiles:
            for tl in tile_buttons:
                tl.state = 0
                tl.display(screen)
                screen.blit(tl.images[1], (tl.pos + pygame.Vector2(8, 8)))
        else:
            i = 0
            for btn in input_buttons:
                btn.display(screen)
            for btn in input_buttons:
                if selected_input == btn.text:
                    break
                i += 1

            show_text(
                screen,
                'Difficulty',
                790, 100, [0, 0, 0], 20
            )
            show_text(
                screen,
                str(level_info['difficulty']),
                795, 130, [0, 0, 0], 20
            )

            show_text(
                screen,
                'Initial Wave',
                790, 160, [0, 0, 0], 20
            )
            show_text(
                screen,
                str(level_info['start_wave']),
                795, 190, [0, 0, 0], 20
            )

            show_text(
                screen,
                'Initial Natural Ingot',
                790, 220, [0, 0, 0], 20
            )
            show_text(
                screen,
                str(level_info['start_money']),
                795, 250, [0, 0, 0], 20
            )

            show_text(
                screen,
                'Initial Hit',
                790, 280, [0, 0, 0], 20
            )
            show_text(
                screen,
                str(level_info['start_hit']),
                795, 310, [0, 0, 0], 20
            )

            if selected_input != None:
                show_text(
                    screen,
                    '|', 791 + 10 * level_name_pos,
                    130 + shift_pos * i, (0, 0, 0), 20
                )
        save_button.display(screen)

        if is_error:
            show_text(screen, 'Error', 300, 175, (0, 0, 0), 108)

        display.blit(pygame.transform.scale(
            screen, display.get_size()), (0, 0))
        pygame.display.update()

        clock.tick(FPS)

    save(map_info, level_info, new_level_name)
    return