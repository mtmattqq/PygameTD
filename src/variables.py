import pygame
import os
from pygame import  DOUBLEBUF, SCALED, FULLSCREEN, QUIT, KEYDOWN, KEYUP
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, MOUSEWHEEL
from pygame import FINGERDOWN, FINGERUP, FINGERMOTION

resolution = (1024, 576)
pygame.init()
pygame.font.init()
pygame.mixer.init()
flags = DOUBLEBUF | SCALED | FULLSCREEN
resolution = (1024, 576)
screen = pygame.surface.Surface(resolution)
display = pygame.display.set_mode(resolution, flags, 32)
screen.fill((245, 245, 245))
clock = pygame.time.Clock()
pygame.display.set_caption("Basic TD Game")
font = 'unifont'
pygame.event.set_allowed([
    QUIT, KEYDOWN, KEYUP,
    MOUSEBUTTONDOWN, MOUSEBUTTONUP,
    MOUSEMOTION, MOUSEWHEEL,
    FINGERDOWN, FINGERUP, FINGERMOTION
])
pygame.display.set_icon(pygame.image.load(
    os.path.join(os.getcwd(), 'AppData', 'icon.png')))
FPS = 60
MOVEMENT = [[1, 0], [0, 1], [-1, 0], [0, -1]]
is_fullscreen = True
volume = 100
clock = pygame.time.Clock()