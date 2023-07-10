import pygame
import copy
from pygame.locals import *
from AppData import vec2D as vec

# pygame init
pygame.init()
flags = FULLSCREEN | DOUBLEBUF | SCALED
resolution = (1980, 1080)
screen = pygame.display.set_mode(resolution, flags, 16)
screen.fill((255, 255, 255))
clock=pygame.time.Clock()
pygame.display.set_caption("Basic TD Game")
font=pygame.font.SysFont('microsoftjhenghei',50)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, MOUSEWHEEL])

# variables
FPS=60
relative_pos = vec.vec2D(0, 0)

def show_text(text = '', x = 0, y = 0, color = (0, 0, 0), size = 0) :
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
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()