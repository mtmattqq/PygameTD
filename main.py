import pygame
import copy

from pygame.locals import *

# pygame init
pygame.init()
flags = FULLSCREEN | DOUBLEBUF
resolution = (1980, 1080)
screen = pygame.display.set_mode(resolution, flags, 16)
screen.fill((255, 255, 255))
pygame.display.set_caption("Basic TD Game")
font=pygame.font.SysFont('microsoftjhenghei',50)

# variables
FPS=60

InGame=True
while InGame:
    # event in pygame
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            InGame=False            
pygame.quit()