import pygame
import os

def show_text(screen, text='', x=0, y=0, color=(0, 0, 0), size=0):
    font = pygame.font.Font(os.path.join(
        os.getcwd(), 'AppData', 'unifont.ttf'), size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.topleft = (x-10, y-20)
    screen.blit(text, textRect)