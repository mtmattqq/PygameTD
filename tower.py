from vec2D import vec2D
import pygame
import os
from tile import TILE_SIZE
import math
import enemy

def do_nothing() :
    return

class tower(pygame.sprite.Sprite) :
    def __init__(
        self, pos = vec2D(0, 0),
        width = 0, hight = 0, 
        pictures = [''],
        damage = 0, reload = 0,
        range = 0, bullet_speed = 0
    ) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.hight = hight
        self.width = width
        self.placed = False
        self.selected = False
        self.damage = damage
        self.reload = reload
        self.range = range
        self.bullet_speed = bullet_speed
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
    
    def action_onclick(self) :
        self.selected = True

    def click(self, pos = vec2D(0, 0)) :
        if(self.detect(pos)) :
            return self.action_onclick()
        else :
            self.selected = False

    def place(self, pos = vec2D(0, 0)) :
        self.pos = pos
        self.placed = True

    def display(self, screen) :
        screen.blit(
            self.images[self.state], 
            (self.pos*TILE_SIZE).get_tuple()
        )

class basic_tower(tower) :
    def __init__(
        self, pos = vec2D(0, 0),
        width = TILE_SIZE, hight = TILE_SIZE, 
        pictures = ['basic_tower16.png', 'basic_tower_barrel.png'],
        damage = 1, reload = 3,
        range = 1.5, bullet_speed = 1
    ) :
        
        super().__init__(
            pos, width, hight, 
            pictures,
            damage, reload,
            range, bullet_speed
        )
        self.aim = vec2D(0, 1)
        self.angle = 0
    def display(self, screen):
        super().display(screen)
        barrel = pygame.transform.rotozoom(self.images[1],self.angle, 1)
        rotated_rect = barrel.get_rect(center = (self.pos*TILE_SIZE).get_tuple())
        dw = rotated_rect.width - self.images[0].get_rect().width
        dw /= 2
        rotated_rect.centerx -= dw
        rotated_rect.centery -= dw
        screen.blit(
            barrel, 
            rotated_rect.center
        )

    def aim_first(self, enemys = []) :
        first_enemy = enemys[0]
        for enemy in enemys :
            if enemy.progress > first_enemy.progress :
                first_enemy = enemy
        relation = first_enemy.pos - (self.pos*TILE_SIZE + vec2D(TILE_SIZE/2,TILE_SIZE/2))
        self.angle = math.atan2(relation.y/relation.x)