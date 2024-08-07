import math
import pygame

PI = math.pi 

def transform(vec = pygame.vector2(0, 0), tile_size = 0) :
    vec = vec*tile_size + pygame.vector2(1, 1)*(tile_size/2)
    return vec