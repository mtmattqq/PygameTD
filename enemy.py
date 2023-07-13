from vec2D import vec2D
from vec2D import dis
import pygame
import os
from tile import TILE_SIZE
import math
import enemy

class enemy :
    def __init__(
        self, pos = vec2D(0, 0),
        width = 0, height = 0, 
        pictures = [''],
        hit = 0, armor = 0,
        shield = 0, move_speed = 0,
        path = []
    ) :
        # pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.height = height
        self.width = width
        self.hit = self.max_hit = hit
        self.armor = armor
        self.shield = self.max_shield = shield
        self.move_speed = move_speed
        self.velocity = vec2D(0, 0)
        self.progress = 0
        self.alive = True
        self.path = path
        self.max_progress = len(path)
        self.images = []
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.width = width
        self.rect.height = height
        self.rect.center = self.pos.get_tuple()
        for picture in pictures :
            self.images.append(pygame.transform.scale(pygame.image.load(
                os.path.join(os.getcwd(),'AppData',picture)).convert_alpha(), (width,height)))
        self.state = 0
        # self.image = self.images[self.state]
        # self.rect = self.image.get_rect()
        # self.rect.topleft = pos
        
    def detect(self, pos = vec2D(0, 0)) :
        self_pos = self.pos*TILE_SIZE
        if(
            pos.x<self_pos.x+self.width and 
            pos.x>self_pos.x and 
            pos.y<self_pos.y+self.height and 
            pos.y>self_pos.y
        ) :
            return True
        return False

    def display(self, screen) :
        self.rect.center = self.pos.get_tuple()
        screen.blit(
            self.images[self.state], 
            self.rect
        )
    
    def check_state(self) :
        if self.hit <= 0 :
            self.alive = False
        return self.alive
    
    def move(self, delta_time) :
        if self.progress >= self.max_progress :
            # deal damage to player's main tower
            self.alive = False
            return
        self.velocity = self.path[self.progress + 1] - self.path[self.progress]
        self.velocity.change_mod(self.move_speed)
        # print(self.velocity.get_tuple())
        if(
            dis(self.path[self.progress + 1] - self.pos, vec2D(0, 0)) <= 
            dis(self.velocity * (delta_time/1000), vec2D(0, 0))
        ) :
            self.pos = self.path[self.progress + 1].copy()
            self.progress += 1
        else :
            self.pos += self.velocity * (delta_time/1000)

class basic_enemy(enemy) :
    def __init__(
        self, pos = vec2D(0, 0),
        hit = 0, armor = 0,
        shield = 0, move_speed = 0,
        path = []
    ) :
        size = TILE_SIZE/2
        width = TILE_SIZE/2
        height = TILE_SIZE/2
        pictures = [
            'basic_enemy16.png', 
            'hit_bar_red.png', 
            'hit_bar_green.png'
        ]

        super().__init__(
            pos, width, height, 
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )

        self.size = size
    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit :
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1], 
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        self.images[2] = pygame.transform.scale(
            self.images[2], 
            (self.size * (self.hit / self.max_hit), self.size)
        )

        screen.blit(
            self.images[2], 
            hit_bar_rect
        )   
        