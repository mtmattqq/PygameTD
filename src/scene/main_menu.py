from src.variables import *
import json
from src.button import button
from src.scene import *
from src.util import show_text

def init_user_settings():
    global is_fullscreen, volume
    input_file = open(os.path.join(
        os.getcwd(), 'AppData', 'setting.json'), 'r')
    input = input_file.read()
    input = json.loads(input)
    input_file.close()

    is_fullscreen = input['is_fullscreen']
    volume = input['volume']


def create_menu_buttons():
    def click_start_button():
        return True
    start_button = button('Start', pygame.Vector2(resolution[0]/2-64, resolution[1]/2-64),
                          [0, 0, 0], 128, 128,
                          ['start_button.png'], click_start_button)
    start_button.pos = pygame.Vector2(
        resolution[0] / 2 - start_button.width / 2,
        resolution[1] / 2 - start_button.height / 2 + 50)
    setting_button = button('setting', pygame.Vector2(resolution[0]/2-64, resolution[1]/2-64),
                            [0, 0, 0], 128, 128,
                            ['setting_button.png'], click_start_button)
    setting_button.pos = pygame.Vector2(
        (resolution[0] / 2) - setting_button.width / 2 + 150,
        (resolution[1] / 2) - setting_button.height / 2 + 50)
    level_editor_button = button('setting', pygame.Vector2(resolution[0]/2-64, resolution[1]/2-64),
                                 [0, 0, 0], 128, 128,
                                 ['level_editor_button.png'], click_start_button)
    level_editor_button.pos = pygame.Vector2(
        (resolution[0] / 2) - level_editor_button.width / 2 - 150,
        (resolution[1] / 2) - level_editor_button.height / 2 + 50)
    return (start_button, setting_button, level_editor_button)


def main_menu(screen, display):
    init_user_settings()

    if is_fullscreen:
        flags = DOUBLEBUF | FULLSCREEN
    else:
        flags = DOUBLEBUF
    display = pygame.display.set_mode(resolution, flags, 32)
    title = 'Basic TD'

    start_button, setting_button, level_editor_button = create_menu_buttons()

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
                start_button.detect(pos=mouse_pos)
                setting_button.detect(mouse_pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.click(mouse_pos):
                    select_level(screen, display)
                elif setting_button.click(mouse_pos):
                    setting(screen, display)
                elif level_editor_button.click(mouse_pos):
                    level_editor(screen, display)

        # display
        screen.fill((245, 245, 245))
        start_button.display(screen)
        setting_button.display(screen)
        level_editor_button.display(screen)
        show_text(screen, title, 300, 175, (0, 0, 0), 108)
        display.blit(pygame.transform.scale(
            screen, display.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    return