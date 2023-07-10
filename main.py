import pygame
import copy

from pygame.locals import *

# pygame init
pygame.init()
flags = FULLSCREEN | DOUBLEBUF
resolution = (1980, 1080)
screen = pygame.display.set_mode(resolution, flags, 16)
screen.fill((255, 255, 255))
clock=pygame.time.Clock()
pygame.display.set_caption("Basic TD Game")
font=pygame.font.SysFont('microsoftjhenghei',50)

# variables
FPS=60
relative_pos = vec2D(0, 0)

def show_text(text = '', x = 0, y = 0, color = (0, 0, 0)) :
    text=font.render(text, True, color)
    textRect=text.get_rect()
    textRect.topleft=(x+relative_pos.x-10, y+relative_pos.y-20)
    screen.blit(text, textRect)

InGame=True
while InGame :
    # event in pygame
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            InGame = False
        if event.type == pygame.KEYDOWN :
            if event.unicode == 'q' :
                InGame = False
    clock.tick(FPS)
pygame.quit()