from src.variables import *
from src.button import button
import json
from src.util import show_text
from pygame.locals import *

def setting(screen, display):
    global flags, is_fullscreen, volume
    fullscreen_button = button(
        'fullscreen', pygame.Vector2(
            resolution[0] / 2 - 128 + 100, resolution[1] / 2 - 16 - 50),
        [0, 0, 0], 256, 32,
        ['select_level.png']
    )
    set_volume_button = button(
        'set_volume_button', pygame.Vector2(
            resolution[0] / 2 - 16 - 100, resolution[1] / 2 - 16 + 50),
        [0, 0, 0], 32, 32,
        ['set_volume.png']
    )

    input_file = open(os.path.join(
        os.getcwd(), 'AppData', 'setting.json'), 'r')
    input = input_file.read()
    input = json.loads(input)
    input_file.close()

    is_fullscreen = input['is_fullscreen']
    volume = input['volume']
    is_set_volume_bar_pressed = False

    title = 'Setting'

    in_game = True
    while in_game:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = pygame.Vector2(mouse_pos[0], mouse_pos[1])

        if is_set_volume_bar_pressed:
            mouse_pos.x
            volume = (mouse_pos.x -
                      (resolution[0] / 2 - 16 - 20)) / 256 * 100 - 7
            volume = max(0, min(100, volume))

        # event in pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if set_volume_button.click(mouse_pos):
                    is_set_volume_bar_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if fullscreen_button.click(mouse_pos):
                    if is_fullscreen:
                        is_fullscreen = False
                        flags = DOUBLEBUF
                    else:
                        is_fullscreen = True
                        flags = DOUBLEBUF | FULLSCREEN
                    display = pygame.display.set_mode(resolution, flags, 32)
                is_set_volume_bar_pressed = False

        # display
        screen.fill((245, 245, 245))
        show_text(screen, title, 330, 70, [0, 0, 0], 108)
        fullscreen_button.display(screen)
        show_text(screen, 'Fullscreen : ', 275, 237, [0, 0, 0], 36)
        show_text(screen, str(is_fullscreen), 580, 237, [0, 0, 0], 36)

        show_text(screen, 'Volume : ', 335, 337, [0, 0, 0], 36)
        show_text(screen, '{:.0f}'.format(volume), 780, 337, [0, 0, 0], 36)
        set_volume_button.pos.x = resolution[0] / \
            2 - 16 - 20 + (volume * 256 / 100)
        pygame.draw.line(
            screen, [0, 0, 0],
            [resolution[0] / 2 - 16, resolution[1] / 2 - 16 + 65],
            [resolution[0] / 2 - 16 + 250, resolution[1] / 2 - 16 + 65], 2
        )
        set_volume_button.display(screen)

        display.blit(pygame.transform.scale(
            screen, display.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)

    input['is_fullscreen'] = is_fullscreen
    input['volume'] = volume
    output = open(os.path.join(os.getcwd(), 'AppData', 'setting.json'), 'w')
    output.write(json.dumps(input))