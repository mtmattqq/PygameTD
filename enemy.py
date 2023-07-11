from vec2D import vec2D
import pygame
import os
from tile import TILE_SIZE
import math
import enemy

class enemy(pygame.sprite.Sprite) :
    def __init__(
        self, pos = vec2D(0, 0),
        width = 0, hight = 0, 
        pictures = [''],
        hit = 0, armor = 0,
        shield = 0, move_speed = 0
    ) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.hight = hight
        self.width = width
        self.hit = self.max_hit = hit
        self.armor = armor
        self.shield = self.max_shield = shield
        self.move_speed = move_speed
        self.velocity = vec2D(0, 0)
        self.progress = 0
        self.images = []
        for picture in pictures :
            self.images.append(pygame.transform.scale(pygame.image.load(
                os.path.join(os.getcwd(),'AppData',picture)).convert_alpha(), (width,hight)))
        self.state = 0
        # self.image = self.images[self.state]
        # self.rect = self.image.get_rect()
        # self.rect.topleft = pos
        
    def detect(self, pos = vec2D(0, 0)) :
        self_pos = self.pos*TILE_SIZE
        if(
            pos.x<self_pos.x+self.width and 
            pos.x>self_pos.x and 
            pos.y<self_pos.y+self.hight and 
            pos.y>self_pos.y
        ) :
            return True
        return False

    def move(self, pos = vec2D(0, 0)) :
        self.pos += pos

    def display(self, screen) :
        screen.blit(
            self.images[self.state], 
            (self.pos*TILE_SIZE).get_tuple()
        )

class basic_enemy(enemy) :
    def __init__(
        self, pos = vec2D(0, 0),
        width = TILE_SIZE/4, hight = TILE_SIZE/4, 
        pictures = ['basic_enemy16.png'],
        hit = 0, armor = 0,
        shield = 0, move_speed = 0
    ) :
        
        super().__init__(
            pos, width, hight, 
            pictures,
            hit, armor,
            shield, move_speed
        )
    def display(self, screen):
        super().display(screen)