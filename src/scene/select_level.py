import os
import json
from src.button import *
from src.util import *
from src.scene import *
from src.scene.level import level

def select_level(screen, display):
    levels_file = open(os.path.join(
        os.getcwd(), 'AppData', 'levels.json'), 'r')
    levels = levels_file.read()
    levels = json.loads(levels)
    levels_file.close()

    select_level_button = []
    level_per_page = levels['level_per_page']
    shift_pos = 70
    for i in range(level_per_page):
        select_level_button.append(
            button(
                '', pygame.Vector2(resolution[0]/2 - 256, 130 + shift_pos * i),
                [0, 0, 0], 512, 64, ['select_level.png']
            )
        )
    page = 0
    max_page = len(levels['file_name']) // level_per_page + 1
    level_num = len(levels['file_name'])
    next_page_button = button(
        "", pygame.Vector2(resolution[0]/2 + 256 - 128,
                           130 + shift_pos * level_per_page),
        [0, 0, 0], 64, 64, ['next_page_button.png']
    )
    prev_page_button = button(
        "", pygame.Vector2(resolution[0]/2 - 256 + 64,
                           130 + shift_pos * level_per_page),
        [0, 0, 0], 64, 64, ['next_page_button.png']
    )
    prev_page_button.images[0] = pygame.transform.flip(
        prev_page_button.images[0], True, False)

    title = 'Select Level'

    in_game = True
    while in_game:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = pygame.Vector2(mouse_pos[0], mouse_pos[1])

        # event in pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # start_button.detect(pos = mouse_pos)
                mouse = pygame.mouse.get_pressed()
            if event.type == pygame.MOUSEBUTTONUP and mouse[0]:
                mouse = [False, False, False]
                if next_page_button.click(mouse_pos):
                    page = (page + 1) % max_page
                elif prev_page_button.click(mouse_pos):
                    page = (page - 1 + max_page) % max_page
                idx = 0
                for btn in select_level_button:
                    if btn.click(mouse_pos):
                        level(screen, display, levels['file_name']
                              [idx + (page * level_per_page)] + '.json')
                        return
                    idx += 1

        # display
        screen.fill((245, 245, 245))
        idx = 0
        for btn in select_level_button:
            if level_num <= idx + (page * level_per_page):
                break
            btn.display(screen)
            show_text(
                screen,
                levels['file_name'][idx + (page * level_per_page)],
                300, 163 + shift_pos * idx, (0, 0, 0), 36
            )
            idx += 1

        next_page_button.display(screen)
        prev_page_button.display(screen)
        show_text(screen, title, 300, 48, (0, 0, 0), 72)
        show_text(
            screen,
            '{} / {}'.format(page + 1, max_page),
            500, 525, (0, 0, 0), 20
        )
        display.blit(pygame.transform.scale(
            screen, display.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    return