import pygame
from src.button import button
from src.variables import resolution, clock, FPS
from src.util import show_text

def game_over(screen, display):
    start_button = button('Start', pygame.Vector2(resolution[0]/2-64, resolution[1]/2-64),
                          [0, 0, 0], 128, 128,
                          ['start_button.png'])
    start_button.pos = pygame.Vector2(
        resolution[0]/2-start_button.width/2,
        resolution[1]/2-start_button.height/2+50)
    title = 'Game Over'

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
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.click(mouse_pos):
                    in_game = False

        # display
        screen.fill((200, 200, 200))
        start_button.display(screen)
        show_text(screen, title, 300, 175, (0, 0, 0), 98)
        display.blit(pygame.transform.scale(
            screen, display.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(FPS)