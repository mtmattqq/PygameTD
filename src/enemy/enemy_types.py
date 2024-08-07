import pygame
from src.enemy import *

def init_enemy_types(level_path):
    return [
        basic_enemy(pygame.Vector2(800, 140), 0, 0, 0, 0, level_path),
        evil_eye(pygame.Vector2(800, 220), 0, 0, 0, 0, level_path),
        high_armor(pygame.Vector2(800, 300), 0, 0, 0, 0, level_path)
    ]

def init_boss_types():
    return [
        basic_boss(pygame.Vector2(785, 80), 0, 0, 0,
                         10, [pygame.Vector2(785, 80)]),
        eye_boss(pygame.Vector2(785, 140), 0, 0, 0,
                       10, [pygame.Vector2(785, 140)]),
        high_armor_boss(pygame.Vector2(785, 200), 0,
                              0, 0, 10, [pygame.Vector2(785, 200)])
    ]