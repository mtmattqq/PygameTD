import pygame
import copy

# pygame init
pygame.init()
screen=pygame.display.set_mode((1000,600))
screen.fill((255,255,255))
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