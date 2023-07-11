import pygame
import copy
from pygame.locals import *
from vec2D import vec2D
from button import button
import tile
import json
import os
import tower

# pygame init
pygame.init()
flags = DOUBLEBUF | SCALED | FULLSCREEN
resolution = (1024, 576)
screen = pygame.display.set_mode(resolution, flags, 16)
screen.fill((245, 245, 245))
clock = pygame.time.Clock()
pygame.display.set_caption("Basic TD Game")
font = 'unifont'
pygame.event.set_allowed([
    QUIT, KEYDOWN, KEYUP, 
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, 
    MOUSEMOTION, MOUSEWHEEL])

# variables
FPS=60
relative_pos = vec2D(0, 0)

def show_text(text = '', x = 0, y = 0, color = (0, 0, 0), size = 0) :
    font=pygame.font.SysFont('unifont', size)
    text=font.render(text, True, color)
    textRect=text.get_rect()
    textRect.topleft=(x+relative_pos.x-10, y+relative_pos.y-20)
    screen.blit(text, textRect)

def level() :
    tile_set = tile.tileset([
        'white.png',
        'main_tower.png',
        'enemy_sourse.png',
        'road.png'
    ], 64, 64)
    level_info_file = open(os.path.join(os.getcwd(), 'AppData', 'basic_level.json'), 'r')
    level_info = level_info_file.read()
    # print(level_info)
    level_info = json.loads(level_info)
    level_info_file.close()

    print(level_info['map_size'])

    level_map = tile.tilemap(tile_set, level_info['map_size'])
    level_map.load(level_info['map'])
    level_map.render()

    # testing 
    t1 = tower.basic_tower(vec2D(4, 5))

    in_game=True
    while in_game :
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2D(mouse_pos[0],mouse_pos[1])

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                in_game = False
            if event.type == pygame.KEYDOWN :
                if event.unicode == 'q' :
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                a=0
            if event.type == pygame.MOUSEBUTTONUP :
                a=0
        
        # display
        screen.fill((245, 245, 245))
        screen.blit(level_map.image, level_map.rect)
        t1.angle += 1
        t1.display(screen)
        # rect = tile_set.tiles[1].get_rect()
        # rect.topleft = (100, 100)
        # screen.blit(tile_set.tiles[1], rect)
        pygame.display.update()
        clock.tick(FPS)
    return

def main_page() :
    def click_start_button() :
        return True
    start_button = button('Start', vec2D(resolution[0]/2-64, resolution[1]/2-64), 
                          [0, 0, 0], 128, 128, 
                          ['start_button.png'], click_start_button)
    start_button.pos = vec2D(
        resolution[0]/2-start_button.width/2, 
        resolution[1]/2-start_button.hight/2+50)
    title = 'Basic TD'

    in_game=True
    while in_game :
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = vec2D(mouse_pos[0],mouse_pos[1])

        # event in pygame
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                in_game = False
            if event.type == pygame.KEYDOWN :
                if event.unicode == 'q' :
                    in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                start_button.detect(pos = mouse_pos+relative_pos)
            if event.type == pygame.MOUSEBUTTONUP :
                if start_button.click(mouse_pos+relative_pos) :
                    level()
        
        # display
        screen.fill((245, 245, 245))
        start_button.display(screen)
        show_text(title, 300, 175, (0, 0, 0), 108)
        pygame.display.update()
        clock.tick(FPS)
    return

main_page()
pygame.quit()